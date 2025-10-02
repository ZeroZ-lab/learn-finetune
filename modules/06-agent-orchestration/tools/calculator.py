from __future__ import annotations

import ast
import operator as op
from typing import Any


OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval(node: ast.AST) -> Any:
    if isinstance(node, ast.Num):  # type: ignore[deprecated]
        return node.n  # type: ignore[attr-defined]
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type not in OPS:
            raise ValueError("unsupported operator")
        return OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


def safe_eval(expr: str) -> float:
    tree = ast.parse(expr, mode="eval")
    return float(_eval(tree.body))  # type: ignore[arg-type]

