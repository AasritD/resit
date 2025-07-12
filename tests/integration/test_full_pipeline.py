import time
import requests

def test_full_pipeline():
    # Give services time to start up
    time.sleep(60)

    # 1. Training: list runs
    r1 = requests.get('http://localhost:8002/api/training/runs/')
    assert r1.status_code == 200
    assert isinstance(r1.json(), list)

    # You'll need a valid JWT here.
    token = "<PASTE_YOUR_JWT_HERE>"
    headers = {'Authorization': f'Bearer {token}'}

    # 2. Inference: upload CSV
    csv_content = 'feature1,feature2,feature3\\n1,2,3'
    files = {'file': ('data.csv', csv_content)}
    r2 = requests.post(
        'http://localhost:8001/inference/api/predict/',
        headers=headers,
        files=files
    )
    assert r2.status_code == 201
    data = r2.json()
    assert 'prediction' in data
    assert 'shap_values' in data

    # 3. Billing: generate invoice
    payload = {"start":"2025-01-01","end":"2025-01-31"}
    r3 = requests.post(
        'http://localhost:8003/billing/api/invoice/generate/',
        headers=headers,
        json=payload
    )
    assert r3.status_code == 201
    inv = r3.json()
    assert 'invoice_id' in inv

    # 4. Users: attempt login (no JWT)
    r4 = requests.get('http://localhost:8004/api/auth/', json={})
    assert r4.status_code in (200, 400)
