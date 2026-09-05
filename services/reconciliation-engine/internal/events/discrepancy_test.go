package events

import "testing"

func TestDemoDiscrepancy(t *testing.T) {
    event := DemoDiscrepancy()
    if event.EventID == "" || event.Type != "amount_drift" { t.Fatalf("unexpected event: %+v", event) }
    if event.Expected-event.Observed != 5 { t.Fatalf("expected amount drift of 5, got %v", event.Expected-event.Observed) }
}
