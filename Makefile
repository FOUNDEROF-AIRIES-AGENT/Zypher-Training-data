.PHONY: install validate generate generate-smoke generate-mega generate-ultra generate-hyper \
        prepare pipeline train-xs index chat serve platform-stats platform-index infer clean

install:
	pip install -r requirements.txt

validate:
	python3 scripts/validate_pipeline.py

generate:
	python3 scripts/generate_corpus.py --scale $(or $(SCALE),1000)

generate-smoke:
	python3 scripts/generate_corpus.py --scale 1000 --max-files 2000

generate-mega:
	python3 scripts/generate_corpus.py --config config/corpus_mega.yaml \
		--mega-multiplier 1000000 --max-files 100000 --skip-wiring --workers 8

generate-ultra:
	python3 scripts/generate_corpus.py --config config/corpus_mega.yaml \
		--mega-multiplier 1000000000 --max-files 1000000 --skip-wiring --workers 16

generate-hyper:
	python3 scripts/generate_corpus.py --config config/corpus_mega.yaml \
		--mega-multiplier 100000000000 --skip-wiring --workers $(or $(WORKERS),32)

prepare:
	python3 scripts/prepare_advanced_dataset.py

pipeline: generate-smoke prepare
	@echo "Pipeline complete."

pipeline-mega: generate-mega index
	@echo "Mega brain ready."

train-xs:
	python3 scripts/train.py --config config/zypher_xs.yaml

index:
	python3 -m zypher.chat --reindex --index-only

chat:
	python3 -m zypher.chat

# Zypher Platform — REST API + jobs + sessions
serve:
		python3 -m zypher_platform serve

platform-stats:
	python3 -m zypher_platform stats

platform-index:
	python3 -m zypher_platform index

infer:
	python3 scripts/infer.py \
		--base-model poolside/Laguna-XS-2.1 \
		--adapter outputs/zypher-xs/final \
		--question "Explain GraphRAG for code architecture."

clean:
	rm -rf data/brain data/platform data/vector_store outputs/ knowledge-base/generated \
		__pycache__ scripts/__pycache__ zypher/__pycache__ brain/__pycache__ zypher_platform/__pycache__
