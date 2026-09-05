package events

import "time"

// DiscrepancyEvent is the versioned contract published to discrepancy.flagged.
type DiscrepancyEvent struct {
	EventID       string    `json:"event_id"`
	SchemaVersion string    `json:"schema_version"`
	DetectedAt    time.Time `json:"detected_at"`
	BranchID      string    `json:"branch_id"`
	GatewayID     string    `json:"gateway_id"`
	TransactionID string    `json:"transaction_id"`
	Type          string    `json:"type"` // duplicate, missing_counterpart, amount_drift, timing_gap
	Expected      float64   `json:"expected_amount,omitempty"`
	Observed      float64   `json:"observed_amount,omitempty"`
	Currency      string    `json:"currency"`
	Details       string    `json:"details"`
	TraceID       string    `json:"trace_id"`
}

func DemoDiscrepancy() DiscrepancyEvent {
	return DiscrepancyEvent{EventID: "demo-evt-001", SchemaVersion: "1.0", DetectedAt: time.Now().UTC(), BranchID: "branch-a", GatewayID: "gateway-01", TransactionID: "txn-1001", Type: "amount_drift", Expected: 125, Observed: 120, Currency: "USD", Details: "Gateway amount differs from canonical ledger amount", TraceID: "trace-demo-001"}
}
