import csv
import os
from pathlib import Path
import streamlit as st

st.set_page_config(page_title='LedgerGuard Observability', layout='wide')

DSN = os.getenv('POSTGRES_DSN', '')
AUDIT_PATH = os.getenv('AUDIT_LOG_PATH', '/app/audit/audit.csv')

def load_metrics() -> tuple[dict[str, str], str]:
    try:
        import psycopg
        with psycopg.connect(DSN, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*), COUNT(*) FILTER (WHERE status = 'resolved'), COUNT(*) FILTER (WHERE discrepancy_type = 'amount_drift') FROM discrepancies")
                total, resolved, drifts = cur.fetchone()
        audited = []
        if Path(AUDIT_PATH).exists():
            with open(AUDIT_PATH, newline='', encoding='utf-8') as handle: audited = list(csv.DictReader(handle))
        nudges = [row for row in audited if row.get('decision') == 'nudge']
        recovered = [row for row in nudges if row.get('action_status') == 'resolved']
        recovery = f'{(len(recovered) / len(nudges) * 100):.1f}%' if nudges else '0.0%'
        return {'Total discrepancies': str(total), 'Resolved': str(resolved), 'Amount drifts': str(drifts), 'Recovery rate': recovery}, 'live Postgres + audit log'
    except Exception as exc:
        return {'Total discrepancies': 'unavailable', 'Resolved': 'unavailable', 'Amount drifts': 'unavailable', 'Recovery rate': 'unavailable'}, f'waiting for live services: {exc}'

st.title('LedgerGuard / ReconCollect AI')
st.caption('Deterministic reconciliation plus policy-grounded discrepancy recovery')
metrics, source = load_metrics()
cols = st.columns(4)
for col, (label, value) in zip(cols, metrics.items()): col.metric(label, value)
st.caption(f'Data source: {source}')
st.subheader('Integration status')
st.info('The dashboard is backed by the discrepancies table and audit log. Refresh after sending the seed event to observe state changes.')
