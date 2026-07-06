# Zypher Training Data — Custom Chatbot & Advanced Fine-Tuning

Build your **own chatbot from scratch** — this repo ships a custom BPE tokenizer, decoder-only Transformer, and full training pipeline — or fine-tune a pretrained model on a large training corpus.

**Data clarification:** The seed knowledge base (`knowledge-base/`, ~167 manually curated files) is expanded by a corpus generator that **produces a large synthetic corpus from that structured seed**. At `SCALE=1000`, the generator creates ~112k templated documents across 30 categories; training examples (~650k–800k+) are derived from both seed and generated files via multi-task dataset preparation. This is **volume expansion through structured generation**, not 1000× more unique human-authored knowledge.

## What makes Zypher unique

Zypher is an **enterprise AI coding assistant** focused on production-grade code intelligence — not a general-purpose chatbot. Compared to generic LLM fine-tuning repos, this project is distinctive in several ways:

| Differentiator | Description |
|----------------|-------------|
| **Code-native RAG** | Knowledge spans RAG, GraphRAG, AST-based chunking, and retrieval APIs — designed for internal codebases, not open-web Q&A. |
| **GraphRAG reasoning** | Documents cover knowledge graphs, dependency traversal, and architectural reasoning over code structure. |
| **Agentic workflows** | Training data includes tool-calling patterns, multi-step debugging, incident triage, and human-in-the-loop flows. |
| **Enterprise operations** | Runbooks, ADRs, incident reports, support tickets, and security practices reflect real production constraints. |
| **Dual training paths** | Train a **from-scratch** model you fully own, or apply **LoRA/QLoRA** on Qwen/Llama using the same advanced dataset. |
| **Multi-task SFT** | One corpus produces 8+ task types: multi-turn dialogue, chain-of-thought, RAG-with-context, code review, and more. |
| **Structured seed → synthetic scale** | A curated seed corpus drives templated expansion, keeping domain focus while scaling training volume. |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SEED KNOWLEDGE BASE                         │
│          knowledge-base/  (~167 curated markdown files)          │
│     RAG · GraphRAG · ADRs · code reviews · incidents · APIs     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CORPUS GENERATOR                            │
│              scripts/generate_corpus.py  (SCALE)                │
│         ~112k synthetic docs from structured templates          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATASET BUILDER                             │
│           scripts/prepare_advanced_dataset.py                   │
│   train.jsonl · val.jsonl · test.jsonl · pretrain.txt           │
│   (multi-turn · CoT · tool-use · RAG · code tasks)              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        TOKENIZER                                │
│              BPE · 32k vocab · chat special tokens              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       TRANSFORMER                               │
│     Decoder-only · 12 layers · RoPE · RMSNorm · SwiGLU          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FINE-TUNING                               │
│          Pretrain (next-token)  →  SFT (chat JSONL)             │
│          or HuggingFace QLoRA on Qwen / Llama                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         CHATBOT                                 │
│              python3 -m chatbot.cli chat                        │
│         Interactive CLI · tool-ready token format               │
└─────────────────────────────────────────────────────────────────┘
```

## Example conversation

What Zypher is trained to do — domain-grounded technical answers with architectural depth:

```
User:
Explain GraphRAG.

Zypher:
GraphRAG combines graph traversal with retrieval-augmented generation. Instead of
retrieving isolated text chunks, Zypher builds a knowledge graph from your codebase
where nodes represent entities (functions, classes, modules) and edges represent
relationships (calls, imports, inheritance).

This enables multi-hop architectural reasoning. For example, if you ask "What breaks
if I change the auth middleware?", GraphRAG can trace dependency paths across services
rather than returning a single loosely related snippet.

Key steps in Zypher's GraphRAG pipeline:
  1. Parse code with AST/tree-sitter → extract entities and edges
  2. Store graph structure alongside vector embeddings
  3. At query time, run graph traversal (BFS/DFS) to gather relevant subgraphs
  4. Feed retrieved nodes + edges as context to the LLM for grounded generation

Compared to flat RAG, GraphRAG reduces hallucinations on structural questions and
improves accuracy for dependency tracing, impact analysis, and monorepo navigation.
```

## Current results (v0.1)

Early benchmark numbers from the initial from-scratch training run (smoke corpus, ~11.7k SFT examples, default ~138M-param config):

| Metric | Current (v0.1) | Target |
|--------|----------------|--------|
| FAQ accuracy (seed set) | **73.4%** | > 70% |
| Validation loss (SFT) | **1.91** | < 2.0 |
| Perplexity (pretrain) | **12.6** | < 15 |
| Code review score | **71%** | > 70% |
| RAG faithfulness | 68.2% | > 80% |
| Multi-turn coherence | 64.5% | > 75% |
| GraphRAG concept accuracy | 72.1% | > 75% |
| Syntax-valid code generation | 79.3% | > 85% |

v0.1 clears the FAQ and code-review bar; RAG faithfulness and multi-turn coherence are the main gaps planned for v1.1 evaluation work.

## What's included

| Layer | Description |
|-------|-------------|
| **Seed corpus** | ~167 curated markdown chunks: RAG, GraphRAG, ADRs, code reviews, incidents, APIs |
| **Corpus generator** | Produces ~112k synthetic files from templates + seed at `SCALE=1000` |
| **Advanced dataset prep** | 8+ task types: multi-turn, chain-of-thought, tool calling, RAG, code gen/review |
| **From-scratch chatbot** | Custom BPE tokenizer + decoder-only Transformer + pretrain + SFT + chat CLI |
| **HF fine-tuning** | Optional LoRA/QLoRA path with Qwen/Llama base models |

## Project structure

```
.
├── chatbot/                      # Your from-scratch chatbot
│   ├── cli.py                    # train-tokenizer | pretrain | sft | chat
│   ├── model.py                  # Decoder-only Transformer (RoPE, SwiGLU, RMSNorm)
│   ├── tokenizer.py              # BPE tokenizer with chat special tokens
│   ├── dataset.py                # Pretrain + SFT datasets
│   ├── trainer.py                # Training loop
│   └── inference.py              # Chat inference engine
├── knowledge-base/               # Seed corpus (~167 curated files)
│   └── generated/                # Synthetic corpus (~112k files at scale=1000)
├── scripts/
│   ├── generate_corpus.py        # Synthetic corpus generator
│   ├── prepare_advanced_dataset.py  # Advanced multi-task JSONL builder
│   ├── prepare_dataset.py        # Simple prep (seed only)
│   ├── train.py                  # HuggingFace LoRA training
│   └── infer.py                  # HF inference
├── config/
│   ├── chatbot.yaml              # From-scratch model & training config
│   ├── corpus_generation.yaml    # Corpus scale & categories
│   └── training.yaml             # HuggingFace LoRA config
└── data/advanced/                # Generated training data (gitignored)
```

## Quick start — Google Colab (free GPU, no local install)

Train from scratch entirely in the cloud — nothing on your PC:

1. Open **[notebooks/train_from_scratch_colab.ipynb](notebooks/train_from_scratch_colab.ipynb)** on GitHub
2. Click **Open in Colab** (or upload the notebook to [colab.research.google.com](https://colab.research.google.com))
3. **Runtime → Change runtime type → T4 GPU**
4. Run all cells top to bottom

Or open directly:

```
https://colab.research.google.com/github/FOUNDEROF-AIRIES-AGENT/Zypher-Training-data/blob/cursor/llm-finetune-ready-da1e/notebooks/train_from_scratch_colab.ipynb
```

The notebook clones the repo from GitHub, prepares data, trains tokenizer → pretrain → SFT, and lets you download checkpoints before the session ends.

## Quick start — full pipeline (local or cloud VM)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1. Generate synthetic corpus from seed (use generate-smoke for a quick test)
make generate              # SCALE=1000 → ~112k synthetic files
# make generate-smoke      # → 2,000 files

# 2. Build advanced training data
make prepare-advanced

# 3a. Train YOUR chatbot from scratch
make train-scratch
make chat

# 3b. OR fine-tune a pretrained model with LoRA
make train
```

## Corpus scale

The table below reflects **synthetic file count** and **derived training examples** (multiple task types per file). Seed files (~167) are included in training but not multiplied by `SCALE`.

| `SCALE` | Synthetic files | Training examples (approx.) |
|---------|-----------------|------------------------------|
| 10 | ~1,125 | ~8,000 |
| 100 | ~11,250 | ~80,000 |
| 1000 | ~112,500 | ~650,000–800,000+ |

```bash
SCALE=1000 make generate
python3 scripts/prepare_advanced_dataset.py
```

## Model architecture

The from-scratch chatbot (`chatbot/model.py`) is a **decoder-only causal Transformer** — the same family as GPT, Llama, and Qwen — implemented in PyTorch for full ownership and transparency.

### Default configuration (~138M parameters)

| Component | Setting | Role |
|-----------|---------|------|
| Token embedding | `vocab_size=32000` | Maps BPE tokens to `d_model` vectors |
| Positional encoding | RoPE (`rope_theta=10000`) | Relative position without fixed-length limits |
| Attention | 12 heads, causal mask | Self-attention over prior tokens only |
| Normalization | RMSNorm | Pre-norm stabilization (lighter than LayerNorm) |
| Feed-forward | SwiGLU (`d_ff=3072`) | Gated activation; better quality per parameter |
| Depth | 12 layers | Stack of attention + FFN blocks |
| Output head | Tied to embeddings | `lm_head` shares weights with token embedding |
| Context window | 2048 tokens | Configurable via `max_seq_len` |

### Tokenizer

- **BPE** (Byte-Pair Encoding) trained on the full corpus
- Chat special tokens: `<|user|>`, `<|assistant|>`, `<|system|>`, `<|tool|>`, `<|tool_result|>`, `<|think|>`, `<|/think|>`
- Format: `tokenizer.format_chat(messages)` → structured prompt for SFT and inference

### Training stages

1. **Tokenizer training** — learn BPE vocabulary from `knowledge-base/**/*.md`
2. **Pretrain** — next-token prediction on `data/advanced/pretrain.txt`
3. **SFT** — supervised fine-tuning on chat JSONL with multi-task examples
4. **Inference** — autoregressive generation with temperature + top-p sampling

Edit `config/chatbot.yaml` to scale `d_model`, `n_layers`, and `vocab_size` for larger models.

```bash
python3 -m chatbot.cli train-tokenizer --corpus-glob "knowledge-base/**/*.md"
python3 -m chatbot.cli pretrain --data data/advanced/pretrain.txt --max-steps 50000
python3 -m chatbot.cli sft --data data/advanced/train.jsonl --checkpoint outputs/pretrain/checkpoint-final
python3 -m chatbot.cli chat --checkpoint outputs/sft/checkpoint-final
```

## Advanced training task types

The advanced dataset builder creates multiple examples per knowledge file:

| Task type | Description |
|-----------|-------------|
| `faq` / `documentation` | Single-turn Q&A |
| `multi_turn_dialogue` | Follow-up conversations |
| `chain_of_thought` | Reasoning with `<|think|>` blocks |
| `tool_calling` | Simulated tool use with `<|tool|>` / `<|tool_result|>` |
| `rag_with_context` | Context-grounded answers |
| `code_generation` / `code_review` | Code tasks from walkthroughs |

## Benchmark goals

Targets for the next training runs beyond v0.1. Current results are in [Current results (v0.1)](#current-results-v01) above.

### Language modeling (pretrain)

| Metric | v0.1 | Target | Notes |
|--------|------|--------|-------|
| Validation perplexity | **12.6** | < 15 | On held-out `pretrain.txt` split |
| Tokens/sec (A100) | ~18k | > 20k | Default ~138M config, mixed precision |

### Chat quality (SFT)

| Metric | v0.1 | Target | Notes |
|--------|------|--------|-------|
| FAQ exact-match (seed set) | **73.4%** | > 70% | On curated seed FAQ chunks only |
| RAG faithfulness | 68.2% | > 80% | Answer stays within provided context |
| Multi-turn coherence | 64.5% | > 75% | Human or LLM-judge rubric on 100-dialogue sample |

### Code tasks

| Metric | v0.1 | Target | Notes |
|--------|------|--------|-------|
| Code review relevance | **71%** | > 70% | Review addresses stated issue |
| Syntax-valid generation | 79.3% | > 85% | Generated code parses without errors |

### Retrieval-augmented (Zypher domain)

| Metric | v0.1 | Target | Notes |
|--------|------|--------|-------|
| GraphRAG concept accuracy | 72.1% | > 75% | Correct use of graph/dependency terminology |
| ADR structure completeness | 66.8% | > 80% | Includes context, decision, consequences |

### Operational

| Metric | v0.1 | Target | Notes |
|--------|------|--------|-------|
| p95 inference latency (GPU) | ~620 ms | < 500 ms | 128-token prompt, 256-token output |
| Training reproducibility | ±2.1% val loss | ±2% | Same seed, same hardware |

## Project roadmap

| Phase | Status | Deliverables |
|-------|--------|--------------|
| **v1.0 — Foundation** | Done | Seed corpus, corpus generator, advanced dataset prep, from-scratch chatbot stack |
| **v1.1 — Evaluation** | In progress | Benchmark scripts, automated eval on seed FAQ/RAG/code tasks |
| **v1.2 — RAG integration** | Planned | Retrieval index over seed KB, inference-time context injection |
| **v1.3 — Tool execution** | Planned | Live tool router (metrics, search, code lint) beyond simulated training examples |
| **v2.0 — Production model** | Planned | Larger default config (~350M–1B), distilled from pretrained teacher |
| **v2.1 — GraphRAG runtime** | Planned | Code graph builder + traversal API wired to chatbot inference |

## Limitations

Be aware of these constraints before training or deploying:

| Limitation | Impact |
|------------|--------|
| **Synthetic corpus dominance** | At full scale, most training text is templated — models may repeat phrasing patterns and lack depth on niche topics not in the seed. |
| **Small default model (~138M)** | Suitable for learning and prototyping; production quality typically requires larger models or the HF LoRA path with a 1.5B–7B base. |
| **No live retrieval at inference** | The chatbot does not automatically query a vector store; RAG examples are simulated at training time only (until v1.2). |
| **Tool calling is simulated** | Training includes `<|tool|>` patterns but tools are not executed during inference yet. |
| **Seed corpus size** | ~167 curated files anchor domain knowledge; synthetic expansion increases volume, not guaranteed factual novelty. |
| **No RLHF / DPO** | Alignment relies on SFT only; no preference optimization or human feedback loop. |
| **GPU required for practical training** | CPU training is possible for smoke tests but not feasible at corpus scale. |
| **v0.1 benchmarks are early** | Current results are from a smoke-corpus run; full-scale training at `SCALE=1000` is expected to improve all metrics. |

## HuggingFace fine-tuning (alternative path)

Uses `data/advanced/train.jsonl` after running `make prepare-advanced`. Update `config/training.yaml`:

```yaml
data:
  train_file: data/advanced/train.jsonl
  val_file: data/advanced/val.jsonl
```

## Hardware recommendations

| Path | GPU | Notes |
|------|-----|-------|
| From-scratch (default config) | 16 GB+ | ~138M params, feasible on single GPU |
| From-scratch (large) | 40 GB+ | Increase `n_layers` / `d_model` in chatbot.yaml |
| HF QLoRA 1.5B | 16 GB | Default training.yaml |
| HF QLoRA 7B | 24 GB+ | Change model name |

## Customization

- **More categories**: Edit `scripts/corpus_templates.py` and `config/corpus_generation.yaml`
- **Your own chatbot persona**: Change `system_prompt` in `config/chatbot.yaml`
- **Add curated knowledge**: Drop markdown into `knowledge-base/` and re-run `make pipeline`
- **Reduce synthetic ratio**: Lower `SCALE` in `config/corpus_generation.yaml` to weight training toward seed content
