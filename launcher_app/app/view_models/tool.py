from py_mvvm.interface import BindingInterface
from launcher_app.app.models.tool import ToolModel


class ToolViewModel:

    def __init__(self, model: ToolModel, binding: BindingInterface):
        self.model = model
        self.tool_list = None
        self.tool_list_bind = binding.new_bind()

    def update_tools(self):
        self.tool_list = self.model.get_tools()
        self.tool_list_bind.update_in_view(self.tool_list)

