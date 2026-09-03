from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get('/health').json()['status'] == 'ok'

def test_query_contract():
    response = client.post('/query', json={'query': 'amount drift policy'})
    assert response.status_code == 200
    assert response.json()['matches'][0]['source'] == 'finance_policy.md'
