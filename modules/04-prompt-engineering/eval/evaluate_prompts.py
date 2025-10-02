import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


@dataclass
class Example:
    text: str
    label: str


def load_testset(path: str) -> list[Example]:
    items: list[Example] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                items.append(Example(obj["text"], obj["label"]))
    return items


def render_template(tpl_path: str, text: str, labels: list[str]) -> str:
    tpl = Path(tpl_path).read_text(encoding="utf-8")
    return tpl.format(text=text, labels=labels)


def call_model(prompt: str, provider: str) -> str:
    """Return raw model output.

    - provider == "dummy": echo a trivial rule-based label for demo
    - otherwise: extend with real provider (e.g., OpenAI) by reading API keys from env
    """
    if provider == "dummy":
        # 简单规则模拟：包含“好/开心”→积极；“烦/差/糟糕/堵车”→消极；否则中性
        text = prompt
        if any(k in text for k in ["开心", "棒", "很好", "真好", "不错"]):
            return "积极"
        if any(k in text for k in ["烦", "差", "糟糕", "堵车", "生气"]):
            return "消极"
        return "中性"
    raise NotImplementedError("Implement provider integration (e.g., OpenAI)")


def extract_label(output: str, json_mode: bool) -> str:
    if json_mode:
        try:
            obj = json.loads(output)
            return str(obj["label"])  # type: ignore
        except Exception:
            return output.strip()
    return output.strip()


def evaluate(
    examples: Iterable[Example],
    provider: str,
    tpl_a: str,
    tpl_b: str,
    labels: list[str],
) -> None:
    total = 0
    correct_a = 0
    correct_b = 0
    for ex in examples:
        total += 1
        pa = render_template(tpl_a, ex.text, labels)
        pb = render_template(tpl_b, ex.text, labels)
        ra = call_model(pa, provider)
        rb = call_model(pb, provider)
        la = extract_label(ra, json_mode=False)
        lb = extract_label(rb, json_mode=True)
        if la == ex.label:
            correct_a += 1
        if lb == ex.label:
            correct_b += 1
    acc_a = correct_a / max(total, 1)
    acc_b = correct_b / max(total, 1)
    print(json.dumps({"acc_a": acc_a, "acc_b": acc_b, "delta": acc_b - acc_a}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="dummy")
    ap.add_argument("--template-a", required=True)
    ap.add_argument("--template-b", required=True)
    ap.add_argument("--testset", required=True)
    ap.add_argument("--labels", default="积极,中性,消极")
    args = ap.parse_args()

    labels = [x.strip() for x in args.labels.split(",") if x.strip()]
    examples = load_testset(args.testset)
    evaluate(examples, args.provider, args.template_a, args.template_b, labels)


if __name__ == "__main__":
    main()

