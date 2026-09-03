# LedgerGuard architecture

## Boundary rule

The Go reconciliation engine and the policy/agent system remain separate services. Kafka is the integration boundary. The engine is authoritative for whether a discrepancy exists; the AI layer is advisory for explanation, severity, and action routing.

## Event flow

```text
transactions -> Kafka -> Go reconciler -> Cassandra canonical state
                              |-> Redis dedup/lookup
                              |-> Postgres discrepancies
                              `-> discrepancy.flagged -> Kafka/HTTP bridge -> n8n
                                                                    |-> FastAPI /query -> embeddings/Pinecone
                                                                    |-> Gemini decision
                                                                    |-> Telegram / Slack / safe correction
                                                                    `-> Google Sheets audit log
Postgres + audit log -> Streamlit metrics dashboard
```

## Reliability and audit rules

Every discrepancy event carries an `event_id`, schema version, timestamp, and trace ID. Consumers should deduplicate on `event_id`, preserve the original payload, and record the AI output alongside the final action. Auto-resolution must be allow-listed, idempotent, and reversible. A policy retrieval failure should route to human review rather than silently resolve.

The repository currently contains intentionally small stubs at each seam. Existing engine, RAG, and notification implementations can replace the stubs behind these contracts without changing the overall topology.
