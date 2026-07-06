"""Pluggable language model providers — reasoning engine only."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class LLMProvider(ABC):
    """Replaceable reasoning engine. Knowledge lives in Zypher Brain."""

    @abstractmethod
    def generate(self, messages: list[dict[str, str]]) -> str:
        ...

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "LLMProvider":
        provider = config.get("provider", "huggingface")
        if provider == "huggingface":
            return HuggingFaceProvider(config)
        raise ValueError(f"Unknown LLM provider: {provider}")


class HuggingFaceProvider(LLMProvider):
    def __init__(self, config: dict[str, Any]):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        self.config = config
        model_cfg = config.get("model", {})
        inf = config.get("inference", {})
        adapter_cfg = config.get("adapter", {})

        self.max_new_tokens = int(inf.get("max_new_tokens", 1024))
        self.temperature = float(inf.get("temperature", 0.3))
        self.top_p = float(inf.get("top_p", 0.9))

        model_name = model_cfg["name"]
        trust = model_cfg.get("trust_remote_code", True)
        use_4bit = model_cfg.get("load_in_4bit", True) and torch.cuda.is_available()

        adapter_path = None
        if adapter_cfg.get("enabled"):
            path = Path(adapter_cfg.get("path", "outputs/zypher-xs/final"))
            if (path / "adapter_config.json").exists():
                adapter_path = path

        tok_src = str(adapter_path) if adapter_path and (adapter_path / "tokenizer_config.json").exists() else model_name
        self.tokenizer = AutoTokenizer.from_pretrained(tok_src, trust_remote_code=trust)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        quant = None
        if use_4bit:
            quant = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quant,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=trust,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        )

        if adapter_path:
            from peft import PeftModel

            self.model = PeftModel.from_pretrained(self.model, str(adapter_path))
        self.model.eval()
        self._uses_adapter = adapter_path is not None

    @property
    def uses_adapter(self) -> bool:
        return self._uses_adapter

    def generate(self, messages: list[dict[str, str]]) -> str:
        import torch

        if hasattr(self.tokenizer, "apply_chat_template") and self.tokenizer.chat_template:
            prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        else:
            parts = [f"{m['role']}: {m['content']}" for m in messages]
            prompt = "\n".join(parts) + "\nassistant:"

        inputs = self.tokenizer(prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        with torch.no_grad():
            out = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=True,
                temperature=self.temperature,
                top_p=self.top_p,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        new_ids = out[0][inputs["input_ids"].shape[1] :]
        return self.tokenizer.decode(new_ids, skip_special_tokens=True).strip()
