import json
from datetime import datetime, timezone

transactions = [
    {'transaction_id': 'txn-1001', 'branch_id': 'branch-a', 'gateway_id': 'gateway-01', 'amount': 125.0, 'currency': 'USD', 'occurred_at': datetime.now(timezone.utc).isoformat()},
    {'transaction_id': 'txn-1001', 'branch_id': 'branch-b', 'gateway_id': 'gateway-02', 'amount': 120.0, 'currency': 'USD', 'occurred_at': datetime.now(timezone.utc).isoformat()},
]
print(json.dumps(transactions, indent=2))
