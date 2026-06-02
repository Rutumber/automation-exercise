import uuid


def test_api_products_list(api_client, base_api_url):
    response = api_client.get(f"{base_api_url}/productsList")
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 200
    assert "products" in payload
    assert isinstance(payload["products"], list)
    assert len(payload["products"]) > 0


def test_api_brands_list(api_client, base_api_url):
    response = api_client.get(f"{base_api_url}/brandsList")
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 200
    assert "brands" in payload
    assert isinstance(payload["brands"], list)
    assert len(payload["brands"]) > 0


def test_api_search_product_returns_matches(api_client, base_api_url):
    response = api_client.post(
        f"{base_api_url}/searchProduct",
        data={"search_product": "top"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 200
    assert "products" in payload
    assert isinstance(payload["products"], list)
    assert any("top" in product["name"].lower() for product in payload["products"])


def test_api_verify_login_invalid_user(api_client, base_api_url):
    response = api_client.post(
        f"{base_api_url}/verifyLogin",
        data={"email": "invalid@example.com", "password": "wrong123"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 404
    assert "User not found" in payload["message"]


def test_api_create_get_delete_account(api_client, base_api_url, api_test_user):
    get_response = api_client.get(
        f"{base_api_url}/getUserDetailByEmail",
        params={"email": api_test_user["email"]},
    )
    assert get_response.status_code == 200

    get_payload = get_response.json()
    assert get_payload["responseCode"] == 200
    assert get_payload["user"]["email"] == api_test_user["email"]
    assert get_payload["user"]["name"] == api_test_user["name"]

    delete_response = api_client.delete(
        f"{base_api_url}/deleteAccount",
        data={"email": api_test_user["email"], "password": api_test_user["password"]},
    )
    assert delete_response.status_code == 200

    delete_payload = delete_response.json()
    assert delete_payload["responseCode"] == 200
    assert "Account deleted" in delete_payload["message"]
