import os
import streamlit as st

st.set_page_config(page_title='LedgerGuard Observability', layout='wide')
st.title('LedgerGuard / ReconCollect AI')
st.caption('Deterministic reconciliation plus policy-grounded discrepancy recovery')

# Replace demo values with Postgres and Google Sheets queries in production.
metrics = [('Reconciliation accuracy', '99.2%', 'canonical matches / total'), ('Recovery rate', '73%', 'nudges resolved / nudges sent'), ('Escalations', '18', 'open + resolved'), ('Median resolution time', '14 min', 'flagged to resolved')]
cols = st.columns(4)
for col, (label, value, help_text) in zip(cols, metrics): col.metric(label, value, help=help_text)
st.subheader('Integration status')
st.info('Demo mode: connect Postgres discrepancies and Google Sheets audit-log adapters before recording measured results.')
