# Deployment

## Docker

```bash
docker-compose up -d
```

## Manual

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
cd frontend && npm run build
```

## Requirements

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
