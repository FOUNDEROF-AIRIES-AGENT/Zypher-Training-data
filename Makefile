.PHONY: install validate generate prepare pipeline train-xs index chat infer clean

install:
	pip install -r requirements.txt

validate:
	python3 scripts/validate_pipeline.py

generate:
	python3 scripts/generate_corpus.py --scale $(or $(SCALE),1000)

generate-smoke:
	python3 scripts/generate_corpus.py --scale 1000 --max-files 2000

prepare:
	python3 scripts/prepare_advanced_dataset.py

pipeline: generate-smoke prepare
	@echo "Pipeline complete. See data/zypher/dataset_stats.json"

# Optional: fine-tune adapter (NOT required — Zypher Brain is primary knowledge source)
train-xs:
	python3 scripts/train.py --config config/zypher_xs.yaml

# Index Zypher Brain (vector + metadata + graph)
index:
	python3 -m zypher.chat --reindex --index-only

# Chat: Zypher Brain retrieval + LLM reasoning engine
chat:
	python3 -m zypher.chat

# Enable fine-tuned adapter in config/llm.yaml (adapter.enabled: true)
infer:
	python3 scripts/infer.py \
		--base-model poolside/Laguna-XS-2.1 \
		--adapter outputs/zypher-xs/final \
		--question "Explain GraphRAG for code architecture."

clean:
	rm -rf data/brain data/vector_store outputs/ knowledge-base/generated \
		__pycache__ scripts/__pycache__ zypher/__pycache__ brain/__pycache__
