"""Minimal LoRA fine-tuning script for causal LM.

Requirements: transformers, peft, datasets, accelerate, bitsandbytes (optional)
This is a teaching-oriented script; tune hyperparameters and add eval as needed.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict

from datasets import load_dataset
from peft import LoraConfig, get_peft_model
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)


@dataclass
class Args:
    model: str
    train_file: str
    output_dir: str
    epochs: int = 1
    batch_size: int = 2
    lr: float = 2e-4
    lora_r: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05


def format_sample(rec: Dict[str, str]) -> str:
    inst = rec.get("instruction", "")
    inp = rec.get("input", "")
    out = rec.get("output", "")
    if inp:
        prompt = f"指令：{inst}\n输入：{inp}\n回答："
    else:
        prompt = f"指令：{inst}\n回答："
    return prompt + out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--train-file", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--batch-size", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--lora-r", type=int, default=8)
    ap.add_argument("--lora-alpha", type=int, default=16)
    ap.add_argument("--lora-dropout", type=float, default=0.05)
    args_ns = ap.parse_args()
    args = Args(**vars(args_ns))

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    ds = load_dataset("json", data_files=args.train_file, split="train")
    ds = ds.map(lambda x: {"text": format_sample(x)})

    def tokenize(ex):
        return tok(ex["text"], truncation=True, max_length=1024)

    ds_tok = ds.map(tokenize, batched=True, remove_columns=ds.column_names)

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        load_in_8bit=False,
        torch_dtype=None,
        device_map="auto",
    )

    lora = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    collator = DataCollatorForLanguageModeling(tok, mlm=False)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        learning_rate=args.lr,
        logging_steps=10,
        save_strategy="epoch",
        fp16=False,
        bf16=False,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds_tok,
        data_collator=collator,
    )

    trainer.train()
    trainer.save_model(args.output_dir)


if __name__ == "__main__":
    main()

