# Deploy Coltex with Docker

## Prerequisites

- Docker 24+ and Docker Compose v2
- 4 GB RAM minimum (8 GB recommended for embedding index builds)

## Quick Start

```bash
git clone <repo> coltex && cd coltex
docker compose up -d --build
curl http://localhost:8080/health
cat data/platform/DEMO_API_KEY.txt
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | Enable OpenAI LLM provider |
| `COLTEX_DATA_DIR` | `/data` | Persistent storage mount |

## Volumes

- `coltex-data` — SQLite DB, tenant collections, vector stores
- `./knowledge-base` — Bundled corpus (read-only)
- `./config` — Brain and platform YAML

## Production Checklist

- [ ] Change `auth.jwt_secret` in `config/platform.yaml`
- [ ] Set `OPENAI_API_KEY` for production LLM
- [ ] Restrict `cors_origins` to your domain
- [ ] Use external volume backup for `coltex-data`
- [ ] Put reverse proxy (nginx/Traefik) with TLS in front
- [ ] Remove or disable demo tenant seeding

## Scaling

Enable the worker profile for a second API instance:

```bash
docker compose --profile scale up -d
```

For production scale, use Kubernetes manifests in `deploy/kubernetes/`.
