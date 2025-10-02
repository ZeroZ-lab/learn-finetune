"""评测 LoRA/QLoRA 微调模型的最小可复现脚本。

功能：
1. 计算给定评测集的 Token-level Perplexity；
2. 进行贪心生成并计算简单的 Exact Match（忽略首尾空白）；
3. 导出逐条预测结果 JSON，便于手动复盘与误差分析。

示例运行：
```bash
python evaluate_model.py \
  --model-path outputs/lora-tinyllama \
  --eval-file data/eval_sample.jsonl \
  --max-new-tokens 128 \
  --report-file outputs/eval_report.json
```
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable, List, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def read_jsonl(path: str | Path) -> List[dict]:
    records: List[dict] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def format_prompt(record: dict) -> Tuple[str, str]:
    """将训练同款模板转为 prompt + target。"""

    if "prompt" in record and "expected" in record:
        return record["prompt"], record["expected"]

    instruction = record.get("instruction", "").strip()
    input_text = record.get("input", "").strip()
    output = record.get("output", "").strip()

    if input_text:
        prompt = (
            "### Instruction:\n"
            f"{instruction}\n\n"
            "### Input:\n"
            f"{input_text}\n\n"
            "### Response:\n"
        )
    else:
        prompt = (
            "### Instruction:\n"
            f"{instruction}\n\n"
            "### Response:\n"
        )
    return prompt, output


def perplexity(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    samples: Iterable[Tuple[str, str]],
    device: torch.device,
) -> float:
    """计算平均 perplexity。"""

    total_log_likelihood = 0.0
    total_tokens = 0

    for prompt, target in samples:
        if not target:
            continue
        prompt_ids = tokenizer(prompt, add_special_tokens=False).input_ids
        batch = tokenizer(
            prompt + target,
            return_tensors="pt",
            truncation=True,
            max_length=tokenizer.model_max_length,
        )
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)

        labels = input_ids.clone()
        labels[:, : len(prompt_ids)] = -100

        with torch.no_grad():
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels,
            )

        target_tokens = (labels != -100).sum().item()
        if target_tokens == 0:
            continue

        total_log_likelihood += outputs.loss.item() * target_tokens
        total_tokens += target_tokens

    if total_tokens == 0:
        raise ValueError("Evaluation set must contain at least one target token")

    avg_loss = total_log_likelihood / total_tokens
    return float(torch.exp(torch.tensor(avg_loss)))


def generate_and_score(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    prompts: Iterable[str],
    device: torch.device,
    *,
    max_new_tokens: int = 128,
) -> List[str]:
    generations: List[str] = []
    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        generated_ids = output[0][inputs["input_ids"].shape[-1] :]
        text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        generations.append(text)
    return generations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned causal LM")
    parser.add_argument("--model-path", required=True, help="本地模型路径或 HF Hub 名称")
    parser.add_argument("--eval-file", required=True, help="评测集 JSONL 文件")
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument(
        "--report-file",
        type=str,
        default=None,
        help="可选，输出逐条预测的 JSON 报告",
    )
    parser.add_argument("--device", type=str, default=None, help="强制指定设备 (cpu/cuda/mps)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.device:
        device = torch.device(args.device)
    else:
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")

    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(args.model_path)
    model.to(device)
    model.eval()

    records = read_jsonl(args.eval_file)
    prompts_targets = [format_prompt(r) for r in records]

    ppl = perplexity(model, tokenizer, prompts_targets, device=device)

    prompts_only = [p for p, _ in prompts_targets]
    predictions = generate_and_score(
        model,
        tokenizer,
        prompts_only,
        device=device,
        max_new_tokens=args.max_new_tokens,
    )

    gold_answers = [t.strip() for _, t in prompts_targets]
    correct = sum(1 for pred, gold in zip(predictions, gold_answers) if pred.strip() == gold)
    total = len(gold_answers)
    exact_match = correct / total if total else 0.0

    summary = {
        "perplexity": ppl,
        "exact_match": exact_match,
        "total_samples": total,
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.report_file:
        report_path = Path(args.report_file)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            for record, prediction in zip(records, predictions):
                payload = dict(record)
                payload["prediction"] = prediction
                payload["correct"] = prediction.strip() == record.get("expected", record.get("output", "")).strip()
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
