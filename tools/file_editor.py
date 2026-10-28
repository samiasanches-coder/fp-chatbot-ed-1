from pathlib import Path

from tools.base_tool import BaseTool


class FileEditorTool(BaseTool):
    name = "file_editor"

    def run(self, text: str):
        target = Path("data/generated/files/edited_file.txt")
        target.parent.mkdir(parents=True, exist_ok=True)
        content = text.replace("write file", "").replace("edit file", "").replace("create file", "").strip() or "This file was created by the chatbot file editor tool."
        target.write_text(content, encoding="utf-8")
        return {"tool": self.name, "status": "enabled", "path": str(target), "message": "File written successfully."}
