import asyncio
import inspect

from .interface import BindingInterface, rsetattr, rgetattr


def is_async():
    try:
        asyncio.get_running_loop()
        return True
    except RuntimeError:
        return False


class Communicator:
    def __init__(self, state, viewmodel_linked_object=None, linked_object_attributes=None,
                 callback_after_update=None):
        self.state = state

        self.linked_object_attributes = None
        if (viewmodel_linked_object and
                not isinstance(viewmodel_linked_object, dict) and
                not inspect.isfunction(viewmodel_linked_object)):
            if not linked_object_attributes:
                self.linked_object_attributes = viewmodel_linked_object.__dict__
            else:
                self.linked_object_attributes = linked_object_attributes

        self.viewmodel_linked_object = viewmodel_linked_object
        self.state_variable_name = None
        self.callback_after_update = callback_after_update

    def on_state_update(self, attribute_name, name_in_state):
        def update(**kwargs):
            rsetattr(self.viewmodel_linked_object, attribute_name, self.state[name_in_state])
            if self.callback_after_update:
                self.callback_after_update(attribute_name)

        return update

    def connect(self, state_variable_name=None):
        # connect should be called from View side to connect a
        # GUI element (via it's name in Trame state object)
        # and a linked_object (passed during bind creation from ViewModel side)
        self.state_variable_name = state_variable_name
        if state_variable_name:
            self.state[self.state_variable_name] = {}
        for attribute_name in self.linked_object_attributes or []:
            name_in_state = self.get_name_in_state(attribute_name)
            self.state[name_in_state] = ""

        # this updates ViewModel on state change
        if self.viewmodel_linked_object:
            if self.linked_object_attributes:
                for attribute_name in self.linked_object_attributes:
                    name_in_state = self.get_name_in_state(attribute_name)
                    f = self.on_state_update(attribute_name, name_in_state)
                    self.state.change(name_in_state)(f)
            else:
                @self.state.change(state_variable_name)
                def update_viewmodel_callback(**kwargs):
                    if isinstance(self.viewmodel_linked_object, dict):
                        self.viewmodel_linked_object.update(kwargs[state_variable_name])
                    elif isinstance(self.viewmodel_linked_object, type(lambda: None)):
                        self.viewmodel_linked_object(kwargs[state_variable_name])
                    else:
                        raise Exception("cannot update", self.viewmodel_linked_object)
                    if self.callback_after_update:
                        self.callback_after_update(state_variable_name)

    def update_in_view(self, value):
        # this updates a View (GUI) when called by a ViewModel
        if self.linked_object_attributes:
            for attribute_name in self.linked_object_attributes:
                name_in_state = self.get_name_in_state(attribute_name)
                value_to_change = rgetattr(value, attribute_name)
                self.set_variable_in_state(name_in_state, value_to_change)
        else:
            self.set_variable_in_state(self.state_variable_name, value)

    def set_variable_in_state(self, name_in_state, value):
        if is_async():
            with self.state:
                self.state[name_in_state] = value
                self.state.dirty(name_in_state)
        else:
            self.state[name_in_state] = value
            self.state.dirty(name_in_state)

    def get_name_in_state(self, attribute_name):
        if self.state_variable_name:
            name_in_state = f"{self.state_variable_name}_{attribute_name.replace('.', '_')}"
        else:
            name_in_state = attribute_name.replace('.', '_')
        return name_in_state


class TrameBinding(BindingInterface):
    def __init__(self, state):
        self._state = state

    def new_bind(self, linked_object=None, linked_object_arguments=None, callback_after_update=None):
        # each new_bind returns an object that can be used to bind a ViewModel/Model variable
        # with a corresponding GUI framework element
        # for Trame we use state to trigger GUI update and linked_object to trigger ViewModel/Model update
        return Communicator(self._state, linked_object, linked_object_arguments, callback_after_update)
