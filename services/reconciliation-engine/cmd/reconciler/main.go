package main

import (
	"encoding/json"
	"log"
	"os"
	"time"

	"ledgerguard/reconciliation-engine/internal/events"
)

func main() {
	// Integration seam: replace this demo output with the existing Raft/Kafka engine.
	e := events.DiscrepancyEvent{
		EventID: "demo-evt-001", SchemaVersion: "1.0", DetectedAt: time.Now().UTC(),
		BranchID: "branch-a", GatewayID: "gateway-01", TransactionID: "txn-1001",
		Type: "amount_drift", Expected: 125.00, Observed: 120.00, Currency: "USD",
		Details: "Gateway amount differs from canonical ledger amount", TraceID: "trace-demo-001",
	}
	payload, err := json.Marshal(e)
	if err != nil { log.Fatal(err) }
	log.Printf("reconciliation engine ready; discrepancy event contract=%s", payload)
	if os.Getenv("DRY_RUN") != "false" { log.Println("DRY_RUN enabled; no external Kafka write") }
}
