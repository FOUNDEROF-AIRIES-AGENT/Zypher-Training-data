.PHONY: install prepare train infer clean

install:
	pip install -r requirements.txt

prepare:
	python3 scripts/prepare_dataset.py

train:
	python3 scripts/train.py --config config/training.yaml

infer:
	python3 scripts/infer.py \
		--base-model Qwen/Qwen2.5-1.5B-Instruct \
		--adapter outputs/zyphersft/final \
		--question "What is Retrieval-Augmented Generation (RAG) for code?"

clean:
	rm -rf data/ outputs/ .venv __pycache__ scripts/__pycache__
