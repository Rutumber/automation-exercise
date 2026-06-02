import pytest
import requests
import uuid

BASE_API_URL = "https://automationexercise.com/api"

@pytest.fixture(scope="session")
def api_client():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()

@pytest.fixture(scope="session")
def base_api_url():
    return BASE_API_URL

@pytest.fixture
def api_test_user(api_client, base_api_url):
    email = f"api_test_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "name": "API Test",
        "email": email,
        "password": "Test1234",
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "January",
        "birth_year": "1990",
        "firstname": "Api",
        "lastname": "Test",
        "company": "ApiCo",
        "address1": "123 Api St",
        "address2": "Suite 1",
        "country": "India",
        "zipcode": "12345",
        "state": "TestState",
        "city": "TestCity",
        "mobile_number": "1234567890",
    }

    create_response = api_client.post(
        f"{base_api_url}/createAccount",
        data=user_data,
    )
    assert create_response.status_code == 200

    create_payload = create_response.json()
    assert create_payload["responseCode"] == 201
    assert "User created" in create_payload["message"]

    yield user_data

    try:
        delete_response = api_client.delete(
            f"{base_api_url}/deleteAccount",
            data={"email": email, "password": user_data["password"]},
        )
        if delete_response.status_code == 200:
            delete_payload = delete_response.json()
            assert delete_payload["responseCode"] == 200
            assert "Account deleted" in delete_payload["message"]
    except Exception:
        pass
