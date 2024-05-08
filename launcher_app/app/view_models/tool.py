from py_mvvm.interface import BindingInterface
from launcher_app.app.models.tool import ToolModel


class ToolViewModel:

    def __init__(self, model: ToolModel, binding: BindingInterface):
        self.model = model
        self.tool_list = None
        self.tool_list_bind = binding.new_bind(self.tool_list)

    def get_tools(self):
        if not self.tool_list:
            self.tool_list = self.model.get_tools()
        return self.tool_list

