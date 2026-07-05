"""Fine-tune a language model on the Zypher knowledge base using LoRA SFT."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
import yaml
from datasets import load_dataset
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from trl import SFTTrainer, setup_chat_format


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def formatting_func_builder(tokenizer):
    def formatting_func(example):
        return tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )

    return formatting_func


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune a causal LM with LoRA")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/training.yaml"),
        help="Training configuration YAML file",
    )
    parser.add_argument("--train-file", type=Path, default=None)
    parser.add_argument("--val-file", type=Path, default=None)
    args = parser.parse_args()

    cfg = load_config(args.config)
    model_name = cfg["model"]["name"]
    train_file = args.train_file or Path(cfg["data"]["train_file"])
    val_file = args.val_file or Path(cfg["data"]["val_file"])
    output_dir = Path(cfg["training"]["output_dir"])

    use_4bit = cfg["model"].get("load_in_4bit", True)
    bf16 = cfg["training"].get("bf16", torch.cuda.is_available())

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    quant_config = None
    if use_4bit and torch.cuda.is_available():
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16 if bf16 else torch.float16,
            bnb_4bit_use_double_quant=True,
        )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quant_config,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True,
        torch_dtype=torch.bfloat16 if bf16 and torch.cuda.is_available() else torch.float32,
    )

    if use_4bit and torch.cuda.is_available():
        model = prepare_model_for_kbit_training(model)

    if cfg["model"].get("use_chat_template", True):
        model, tokenizer = setup_chat_format(model, tokenizer)

    lora_cfg = cfg["lora"]
    peft_config = LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["alpha"],
        lora_dropout=lora_cfg.get("dropout", 0.05),
        bias="none",
        task_type=TaskType.CAUSAL_LM,
        target_modules=lora_cfg["target_modules"],
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    data_files = {"train": str(train_file)}
    if val_file.exists():
        data_files["validation"] = str(val_file)

    dataset = load_dataset("json", data_files=data_files)
    train_dataset = dataset["train"]
    eval_dataset = dataset["validation"] if "validation" in dataset else None

    train_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=cfg["training"]["num_train_epochs"],
        per_device_train_batch_size=cfg["training"]["per_device_train_batch_size"],
        per_device_eval_batch_size=cfg["training"].get("per_device_eval_batch_size", 1),
        gradient_accumulation_steps=cfg["training"]["gradient_accumulation_steps"],
        learning_rate=cfg["training"]["learning_rate"],
        warmup_ratio=cfg["training"].get("warmup_ratio", 0.03),
        logging_steps=cfg["training"].get("logging_steps", 10),
        save_steps=cfg["training"].get("save_steps", 100),
        eval_strategy="steps" if eval_dataset is not None else "no",
        eval_steps=cfg["training"].get("eval_steps", 100),
        save_total_limit=cfg["training"].get("save_total_limit", 2),
        bf16=bf16 and torch.cuda.is_available(),
        fp16=not bf16 and torch.cuda.is_available(),
        gradient_checkpointing=cfg["training"].get("gradient_checkpointing", True),
        report_to=cfg["training"].get("report_to", "none"),
        optim=cfg["training"].get("optim", "paged_adamw_8bit" if use_4bit else "adamw_torch"),
        max_grad_norm=cfg["training"].get("max_grad_norm", 1.0),
        seed=cfg["training"].get("seed", 42),
    )

    trainer = SFTTrainer(
        model=model,
        args=train_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        formatting_func=formatting_func_builder(tokenizer),
        max_seq_length=cfg["training"].get("max_seq_length", 2048),
        packing=cfg["training"].get("packing", False),
    )

    trainer.train()
    trainer.save_model(str(output_dir / "final"))
    tokenizer.save_pretrained(str(output_dir / "final"))

    print(f"Training complete. Adapter saved to {output_dir / 'final'}")


if __name__ == "__main__":
    main()
