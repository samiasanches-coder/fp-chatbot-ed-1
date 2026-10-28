from __future__ import annotations

import ast
import operator

from tools.base_tool import BaseTool

_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculatorTool(BaseTool):
    name = "calculator"

    def _safe_eval(self, expression: str):
        def _eval(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BIN_OPS:
                return _ALLOWED_BIN_OPS[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY_OPS:
                return _ALLOWED_UNARY_OPS[type(node.op)](_eval(node.operand))
            raise ValueError(f"Unsupported expression: {expression}")

        return _eval(ast.parse(expression, mode="eval").body)

    def run(self, text: str):
        expression = text.replace("calculate", "").replace("math", "").replace("sum", "").strip()
        if not expression:
            return {"tool": self.name, "status": "enabled", "result": "No expression provided."}
        try:
            result = self._safe_eval(expression)
            return {"tool": self.name, "status": "enabled", "expression": expression, "result": result}
        except Exception as exc:
            return {"tool": self.name, "status": "error", "message": str(exc)}
