import csv
import os
from datetime import datetime, timezone

FIELDS = ['event_id', 'decision', 'severity', 'explanation', 'action_status', 'recorded_at']

def write_audit(record: dict, path: str = 'integrations/audit/audit.csv') -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    row = {key: record.get(key, '') for key in FIELDS}
    row['recorded_at'] = datetime.now(timezone.utc).isoformat()
    exists = os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if not exists: writer.writeheader()
        writer.writerow(row)
