package main

import (
    "context"
    "encoding/json"
    "log"
    "os"
    "time"

    "github.com/jackc/pgx/v5"
    "github.com/segmentio/kafka-go"
    "ledgerguard/reconciliation-engine/internal/events"
)

func main() {
    ctx := context.Background()
    event := events.DemoDiscrepancy()
    dsn := getenv("POSTGRES_DSN", "postgres://LedgerGuard:LedgerGuard@postgres:5432/LedgerGuard?sslmode=disable")
    brokers := getenv("KAFKA_BROKERS", "kafka:9092")
    topic := getenv("KAFKA_TOPIC", "discrepancy.flagged")

    conn, err := pgx.Connect(ctx, dsn)
    if err != nil { log.Fatalf("postgres connect: %v", err) }
    defer conn.Close(ctx)
    if err := ensureSchema(ctx, conn); err != nil { log.Fatalf("schema: %v", err) }

    inserted, err := persistDiscrepancy(ctx, conn, event)
    if err != nil { log.Fatalf("persist discrepancy: %v", err) }
    if !inserted { log.Printf("duplicate event ignored: %s", event.EventID); return }

    payload, _ := json.Marshal(event)
    writer := &kafka.Writer{Addr: kafka.TCP(brokers), Topic: topic, Balancer: &kafka.Hash{}, RequiredAcks: kafka.RequireOne}
    defer writer.Close()
    if err := writer.WriteMessages(ctx, kafka.Message{Key: []byte(event.EventID), Value: payload, Time: time.Now()}); err != nil {
        log.Fatalf("publish discrepancy: %v", err)
    }
    log.Printf("published discrepancy event_id=%s topic=%s", event.EventID, topic)
}

func ensureSchema(ctx context.Context, conn *pgx.Conn) error {
    _, err := conn.Exec(ctx, `CREATE TABLE IF NOT EXISTS discrepancies (
        event_id TEXT PRIMARY KEY, transaction_id TEXT NOT NULL, branch_id TEXT NOT NULL,
        gateway_id TEXT NOT NULL, discrepancy_type TEXT NOT NULL, expected_amount NUMERIC(18,2),
        observed_amount NUMERIC(18,2), currency TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'flagged',
        detected_at TIMESTAMPTZ NOT NULL, resolved_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT now())`)
    return err
}

func persistDiscrepancy(ctx context.Context, conn *pgx.Conn, e events.DiscrepancyEvent) (bool, error) {
    result, err := conn.Exec(ctx, `INSERT INTO discrepancies
        (event_id, transaction_id, branch_id, gateway_id, discrepancy_type, expected_amount, observed_amount, currency, detected_at)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) ON CONFLICT (event_id) DO NOTHING`,
        e.EventID, e.TransactionID, e.BranchID, e.GatewayID, e.Type, e.Expected, e.Observed, e.Currency, e.DetectedAt)
    return result.RowsAffected() == 1, err
}

func getenv(key, fallback string) string { if value := os.Getenv(key); value != "" { return value }; return fallback }
