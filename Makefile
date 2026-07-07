.PHONY: install clean index retrieve stats \
        platform platform-dev docker-build docker-up \
        test \
        generate generate-smoke generate-mega generate-ultra generate-hyper \
        expand-curated-kb \
        product product-premium product-premium-smoke product-hyper stream-premium \
        chunks deduplicate validate-product export-graph embeddings benchmarks \
        manifest evaluate audit-distribution

install:
	pip install -r requirements.txt

# Coltex Platform — RAG-as-a-Service API
platform:
	python3 -m coltex_platform

platform-dev:
	python3 -m coltex_platform --reload

docker-build:
	docker compose build

docker-up:
	docker compose up -d

test:
	pytest tests/ -v --tb=short

clean:
	rm -rf data/brain data/vector_store knowledge-base/generated data/product \
		__pycache__ scripts/__pycache__ brain/__pycache__ scripts/product/__pycache__

# Coltex — index and query the RAG database
index:
	python3 -m brain index --reindex

retrieve:
	python3 -m brain retrieve "$(QUERY)"

stats:
	python3 -m brain stats

# Corpus generation (raw markdown expansion)
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

# Expand curated seed knowledge-base with high-quality CHUNK documents
expand-curated-kb:
	python3 scripts/expand_curated_kb.py --count $(or $(COUNT),120)

# Product pipeline — export distributable RAG dataset artifacts
product:
	python3 scripts/product/build_product.py

product-premium-smoke:
	python3 scripts/product/build_premium_product.py --config config/product_hyper_smoke.yaml --skip-embeddings

product-premium:
	python3 scripts/product/build_premium_product.py --config config/product_hyper.yaml

product-hyper:
	python3 scripts/product/build_premium_product.py --config config/product_hyper.yaml --max-files 0

stream-premium:
	python3 scripts/product/stream_premium_corpus.py --config config/product_hyper.yaml

chunks:
	python3 scripts/product/chunk_documents.py

deduplicate:
	python3 scripts/product/deduplicate.py

validate-product:
	python3 scripts/product/validate_quality.py

export-graph:
	python3 scripts/product/export_graph.py

embeddings:
	python3 scripts/product/export_embeddings.py

benchmarks:
	python3 scripts/product/build_benchmarks.py

manifest:
	python3 scripts/product/build_manifest.py

evaluate:
	python3 scripts/product/evaluate_rag.py

audit-distribution:
	python3 scripts/product/audit_distribution.py
