from tools.base_tool import BaseTool


class FileEditorPlugin(BaseTool):
    name = "file_editor"

    def run(self, text: str):
        return {
            "tool": self.name,
            "status": "enabled",
            "message": "File editing is enabled. Use your application logic to write or update files safely.",
        }
