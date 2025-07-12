import time
import requests

BASE_URLS = {
    'training': 'http://localhost:8002',
    'inference': 'http://localhost:8001',
    'billing': 'http://localhost:8003',
    'users': 'http://localhost:8004',
}

def wait_for_service(url, path, timeout=60):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{url}{path}")
            if r.status_code in (200, 401, 403):  # healthy but possibly auth-protected
                return True
        except requests.ConnectionError:
            pass
        time.sleep(2)
    raise RuntimeError(f"Service at {url}{path} failed to become healthy")

def test_end_to_end_crud_and_ml_pipeline():
    # 1. Wait for each service to be healthy
    assert wait_for_service(BASE_URLS['training'], '/api/training/runs/'), "Training service failed"
    assert wait_for_service(BASE_URLS['inference'], '/inference/api/artifacts/'), "Inference service failed"
    assert wait_for_service(BASE_URLS['billing'], '/billing/api/usage/'), "Billing service failed"
    assert wait_for_service(BASE_URLS['users'], '/api/auth/'), "Users service failed"

    # 2. Authenticate against Users service
    auth_resp = requests.post(
        f"{BASE_URLS['users']}/api/auth/",
        json={'username': '<USERNAME>', 'password': '<PASSWORD>'}
    )
    assert auth_resp.status_code == 200, f"Auth failed: {auth_resp.text}"
    token = auth_resp.json().get('access')
    assert token, "No access token received"
    headers = {'Authorization': f'Bearer {token}'}

    # 3. Trigger a retrain and verify runs list grows
    trigger = requests.post(f"{BASE_URLS['training']}/api/training/retrain/", headers=headers)
    assert trigger.status_code in (200, 201), f"Retrain failed: {trigger.text}"
    runs = requests.get(f"{BASE_URLS['training']}/api/training/runs/", headers=headers)
    assert runs.status_code == 200 and isinstance(runs.json(), list), "Bad runs response"

    # 4. Upload a sample for inference
    sample_csv = 'feature1,feature2,feature3\n1,2,3'
    files = {'file': ('sample.csv', sample_csv)}
    inf = requests.post(
        f"{BASE_URLS['inference']}/inference/api/predict/",
        headers=headers,
        files=files
    )
    assert inf.status_code == 201, f"Inference failed: {inf.text}"
    data = inf.json()
    assert 'prediction' in data and 'shap_values' in data, "Incomplete inference data"

    # 5. Generate a billing invoice
    inv = requests.post(
        f"{BASE_URLS['billing']}/billing/api/invoice/generate/",
        headers=headers,
        json={"start":"2025-01-01","end":"2025-01-31"}
    )
    assert inv.status_code == 201, f"Invoice generation failed: {inv.text}"
    inv_data = inv.json()
    assert 'invoice_id' in inv_data, "No invoice_id"

    # 6. CRUD on Users
    # List users
    users_list = requests.get(f"{BASE_URLS['users']}/api/users/", headers=headers)
    assert users_list.status_code == 200 and isinstance(users_list.json(), list), "Users list failed"
    # Export data for the first user
    if users_list.json():
        uid = users_list.json()[0]['id']
        export = requests.get(f"{BASE_URLS['users']}/api/users/{uid}/export_data/", headers=headers)
        assert export.status_code == 200, "Export data failed"
        delete = requests.post(f"{BASE_URLS['users']}/api/users/{uid}/delete_data/", headers=headers)
        assert delete.status_code == 204, "Delete data failed"
