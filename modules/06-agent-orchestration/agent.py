from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from typing import Any, Dict, List

from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
sys.path.append(str(BASE))
sys.path.append(str(BASE.parent))

from tools.calculator import safe_eval
from tools.retrieval_stub import retrieve
from replay_logger import ReplayLogger


@dataclass
class ToolCall:
    name: str
    input: str
    output: str


class Orchestrator:
    def __init__(self):
        self.logger = ReplayLogger()

    def decide(self, query: str) -> str:
        q = query.lower()
        if any(k in q for k in ["计算", "calc", "*", "+", "-", "/"]):
            return "calculator"
        if any(k in q for k in ["查", "搜索", "介绍", "是什么"]):
            return "retrieve"
        return "calculator" if any(ch.isdigit() for ch in q) else "retrieve"

    def run_tool(self, name: str, arg: str) -> str:
        if name == "calculator":
            return str(safe_eval(arg))
        if name == "retrieve":
            return retrieve(arg)
        raise ValueError(f"unknown tool: {name}")

    def run(self, query: str, max_steps: int = 3) -> Dict[str, Any]:
        self.logger.log({"event": "start", "query": query, "ts": time.time()})
        thoughts: List[str] = []
        calls: List[ToolCall] = []
        answer = None

        for step in range(max_steps):
            tool = self.decide(query)
            thoughts.append(f"Step {step+1}: choose {tool}")
            out = self.run_tool(tool, query)
            calls.append(ToolCall(tool, query, out))
            self.logger.log({"event": "tool", "name": tool, "input": query, "output": out, "step": step + 1})

            if tool == "calculator":
                answer = f"计算结果：{out}"
                break
            if tool == "retrieve":
                # 演示：一次检索后直接生成回答
                answer = f"基于检索：{out}"
                break

        if answer is None:
            answer = "未得到答案"

        result = {
            "answer": answer,
            "steps": len(calls),
            "calls": [c.__dict__ for c in calls],
            "thoughts": thoughts,
        }
        self.logger.log({"event": "end", "result": result, "ts": time.time()})
        return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    args = ap.parse_args()

    orch = Orchestrator()
    res = orch.run(args.query)
    print(res)


if __name__ == "__main__":
    main()
