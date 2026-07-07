.PHONY: install clean index retrieve stats report \
        corpus corpus-advanced corpus-grow corpus-mega corpus-report \
        product product-personal product-professional product-enterprise product-premium product-premium-smoke product-hyper \
        chunks deduplicate validate-product export-graph embeddings benchmarks \
        manifest evaluate audit-distribution

install:
	pip install -r requirements.txt

clean:
	rm -rf data/brain data/vector_store knowledge-base/generated data/product \
		__pycache__ scripts/__pycache__ brain/__pycache__ scripts/product/__pycache__

# Coltex Knowledge Corpus
corpus:
	python3 scripts/knowledge_corpus.py bootstrap --grow 300

corpus-advanced:
	python3 scripts/knowledge_corpus.py advanced --grow 500

corpus-grow:
	python3 scripts/knowledge_corpus.py grow --count $(or $(COUNT),200)

corpus-mega:
	python3 scripts/knowledge_corpus.py bootstrap --grow 10000

corpus-report:
	python3 scripts/knowledge_corpus.py map
	python3 -m brain report

corpus-structure:
	python3 scripts/knowledge_corpus.py structure

corpus-links:
	python3 scripts/knowledge_corpus.py graph-links

# Coltex Runtime CLI
runtime-status:
	python3 -m runtime status

runtime-health:
	python3 -m runtime health

runtime-curator:
	python3 -m runtime curator

runtime-events:
	python3 -m runtime events --simulate

runtime-dna:
	python3 -m runtime dna --limit 3

# Coltex retrieval engine
index:
	python3 -m brain index --reindex

retrieve:
	python3 -m brain retrieve "$(QUERY)"

stats:
	python3 -m brain stats

report:
	python3 -m brain report

# Corpus generation
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

expand-curated-kb:
	python3 scripts/expand_curated_kb.py --count $(or $(COUNT),120)

product:
	python3 scripts/product/build_product.py

product-personal:
	python3 scripts/product/build_enterprise_product.py --config config/product_personal.yaml --skip-embeddings

product-professional:
	python3 scripts/product/build_enterprise_product.py --config config/product_professional.yaml --skip-embeddings

product-enterprise:
	python3 scripts/product/build_enterprise_product.py --config config/product_enterprise.yaml

product-enterprise-fast:
	python3 scripts/product/build_enterprise_product.py --config config/product_enterprise.yaml --skip-embeddings

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
