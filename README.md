# Zypher Knowledge Base — LLM Fine-Tuning

Fine-tune a language model on the Zypher enterprise RAG / GraphRAG knowledge base using LoRA supervised fine-tuning (SFT).

## Project structure

```
.
├── knowledge-base/          # Source markdown chunks (167 documents)
├── scripts/
│   ├── prepare_dataset.py   # Convert chunks → train/val/test JSONL
│   ├── train.py             # LoRA SFT training with Hugging Face TRL
│   └── infer.py             # Run inference with a fine-tuned adapter
├── config/
│   └── training.yaml        # Model, LoRA, and training hyperparameters
├── data/                    # Generated datasets (gitignored)
└── outputs/                 # Checkpoints and adapters (gitignored)
```

## Quick start

### 1. Install dependencies

Requires Python 3.10+ and a CUDA GPU (recommended: 16 GB+ VRAM for QLoRA).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Prepare the dataset

Converts knowledge-base markdown into chat-format JSONL with task types including FAQ, documentation, architecture decisions, code reviews, incident reports, and support tickets.

```bash
make prepare
# or
python scripts/prepare_dataset.py --kb-dir knowledge-base --output-dir data
```

Outputs:

- `data/train.jsonl`
- `data/val.jsonl`
- `data/test.jsonl`
- `data/dataset_stats.json`

### 3. Train

Default base model: [Qwen/Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) with 4-bit QLoRA.

```bash
make train
# or
python scripts/train.py --config config/training.yaml
```

Edit `config/training.yaml` to change the base model, LoRA rank, learning rate, epochs, or batch size.

### 4. Inference

```bash
python scripts/infer.py \
  --base-model Qwen/Qwen2.5-1.5B-Instruct \
  --adapter outputs/zyphersft/final \
  --question "How does Zypher use GraphRAG for architectural reasoning?"
```

## Training data format

Each JSONL row uses the chat messages format expected by TRL `SFTTrainer`:

```json
{
  "messages": [
    {"role": "system", "content": "You are Zypher..."},
    {"role": "user", "content": "What is RAG for code?"},
    {"role": "assistant", "content": "RAG for code enhances LLMs by..."}
  ],
  "metadata": {
    "source": "CHUNK-00000-....md",
    "chunk_ids": ["CHUNK-00000"],
    "task_type": "faq"
  }
}
```

## Hardware notes

| Setup | Base model | Notes |
|-------|------------|-------|
| 8 GB GPU | `Qwen/Qwen2.5-0.5B-Instruct` | Reduce `max_seq_length` to 1024 |
| 16 GB GPU | `Qwen/Qwen2.5-1.5B-Instruct` | Default config |
| 24 GB+ GPU | `Qwen/Qwen2.5-7B-Instruct` | Set `load_in_4bit: true` |

For CPU-only smoke tests, set `load_in_4bit: false` in `config/training.yaml` and use a very small model — full training on CPU is not practical.

## Customization

- **Different base model**: Update `model.name` in `config/training.yaml`. Adjust `lora.target_modules` if needed for non-LLaMA/Qwen architectures.
- **More data**: Add markdown chunks under `knowledge-base/` and re-run `make prepare`.
- **Experiment tracking**: Uncomment `wandb` in `requirements.txt` and set `training.report_to: wandb`.

## Source data

The `knowledge-base/` directory contains production-ready Zypher documentation covering RAG, GraphRAG, agentic workflows, architecture decisions, code reviews, incidents, and operational runbooks. The preparation script groups related chunks (e.g., ADR context/decision/consequences) into composite training examples.
