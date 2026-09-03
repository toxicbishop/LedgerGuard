# LedgerGuard

LedgerGuard connects a deterministic distributed-ledger reconciliation engine to a policy-grounded AI decision layer without replacing either system.

## Architecture

- **Reconciliation engine (Go):** consumes transaction events, applies deterministic matching and consensus, persists canonical state, and emits structured discrepancy events.
- **Agent orchestration (n8n):** receives discrepancy events, retrieves policy context, asks an LLM for an explanation and recommendation, routes nudge/escalate/auto-resolve actions, and records an audit trail.
- **Policy RAG service (FastAPI):** stateless `/query` API. The Pinecone and Gemini clients are intentionally replaceable stubs for local development.
- **Observability (Streamlit):** reads discrepancy and audit data and exposes accuracy, recovery, escalation, and time-to-resolution metrics.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

The local stack exposes:

| Service | URL / port | Purpose |
|---|---:|---|
| Policy RAG API | `http://localhost:8000` | Policy retrieval contract |
| Kafka HTTP bridge | `http://localhost:8081` | Kafka topic to n8n webhook adapter |
| Streamlit dashboard | `http://localhost:8501` | Demo metrics view |
| n8n | `http://localhost:5678` | Workflow runner |
| Postgres | `localhost:5432` | Discrepancy and audit persistence |
| Kafka | `localhost:9092` | Event transport |

The Go reconciler is scaffolded separately and can be run locally with `go run ./cmd/reconciler`. The compose profile `engine` builds and runs it when Docker is available.

## Event contract

The canonical event is documented in `reconciliation-engine/internal/events/discrepancy.go`. Producers must publish JSON to `discrepancy.flagged`; consumers must treat `event_id` as the idempotency key.

## Demo flow

1. Publish a transaction pair or use `mock-data/generate_transactions.py`.
2. The reconciler emits a `discrepancy.flagged` event.
3. The bridge forwards the event to the n8n intake webhook.
4. n8n calls `/query`, obtains policy context, and invokes the configured LLM node.
5. The decision branch nudges, escalates, or auto-resolves, then writes the decision to the audit log.
6. Streamlit surfaces recovery and resolution metrics.

Local integrations default to dry-run behavior. Configure Telegram, Slack, Google Sheets, Pinecone, Gemini, and n8n credentials through `.env` before enabling external actions.


## License

This project is licensed under the **MIT LICENCE** — see the [LICENSE](LICENSE) file for details.
