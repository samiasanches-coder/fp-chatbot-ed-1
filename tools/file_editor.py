from tools.base_tool import BaseTool


class CalculatorPlugin(BaseTool):
    name = "calculator"

    def run(self, text: str):
        expression = text.replace("calculate", "").replace("math", "").strip()
        if not expression:
            return {"tool": self.name, "status": "enabled", "result": "No expression provided."}
        try:
            result = eval(expression, {}, {})
        except Exception as exc:
            result = str(exc)
        return {"tool": self.name, "status": "enabled", "expression": expression, "result": result}
