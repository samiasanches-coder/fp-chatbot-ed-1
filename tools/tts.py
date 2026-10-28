class BaseTool:
    name = "base_tool"

    def run(self, *args, **kwargs):
        return {"tool": self.name, "status": "not_implemented"}
