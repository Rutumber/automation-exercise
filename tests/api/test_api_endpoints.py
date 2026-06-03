import uuid


def _generate_test_user_data():
    email = f"api_test_{uuid.uuid4().hex[:8]}@example.com"
    return {
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


def _create_user(api_client, base_api_url, user_data):
    return api_client.post(f"{base_api_url}/createAccount", data=user_data)


def _delete_user(api_client, base_api_url, user_data):
    return api_client.delete(
        f"{base_api_url}/deleteAccount",
        data={"email": user_data["email"], "password": user_data["password"]},
    )


def test_api_products_list(api_client, base_api_url):
    response = api_client.get(f"{base_api_url}/productsList")
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 200
    assert "products" in payload
    assert isinstance(payload["products"], list)
    assert len(payload["products"]) > 0


def test_api_products_list_post_method_not_supported(api_client, base_api_url):
    response = api_client.post(f"{base_api_url}/productsList")
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 405
    assert "not supported" in payload["message"].lower()


def test_api_brands_list(api_client, base_api_url):
    response = api_client.get(f"{base_api_url}/brandsList")
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 200
    assert "brands" in payload
    assert isinstance(payload["brands"], list)
    assert len(payload["brands"]) > 0


def test_api_brands_list_put_method_not_supported(api_client, base_api_url):
    response = api_client.put(f"{base_api_url}/brandsList")
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 405
    assert "not supported" in payload["message"].lower()


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


def test_api_search_product_without_parameter(api_client, base_api_url):
    response = api_client.post(f"{base_api_url}/searchProduct", data={})
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 400
    assert "search_product parameter is missing" in payload["message"].lower()


def test_verify_login_valid_user(api_client, base_api_url, api_test_user):
    response = api_client.post(
        f"{base_api_url}/verifyLogin",
        data={"email": api_test_user["email"], "password": api_test_user["password"]},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 200
    assert "user" in payload["message"].lower()


def test_verify_login_without_email_parameter(api_client, base_api_url):
    response = api_client.post(
        f"{base_api_url}/verifyLogin",
        data={"password": "Test1234"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 400
    assert "email or password parameter is missing" in payload["message"].lower()


def test_verify_login_delete_method_not_supported(api_client, base_api_url):
    response = api_client.delete(f"{base_api_url}/verifyLogin")
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 405
    assert "not supported" in payload["message"].lower()


def test_verify_login_invalid_user(api_client, base_api_url):
    response = api_client.post(
        f"{base_api_url}/verifyLogin",
        data={"email": "invalid@example.com", "password": "wrong123"},
    )
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 404
    assert "user not found" in payload["message"].lower()


def test_api_create_user_account(api_client, base_api_url):
    user_data = _generate_test_user_data()
    response = _create_user(api_client, base_api_url, user_data)
    assert response.status_code == 200

    payload = response.json()
    assert payload["responseCode"] == 201
    assert "user created" in payload["message"].lower()

    delete_response = _delete_user(api_client, base_api_url, user_data)
    assert delete_response.status_code == 200
    assert delete_response.json()["responseCode"] == 200


def test_api_delete_user_account(api_client, base_api_url):
    user_data = _generate_test_user_data()
    create_response = _create_user(api_client, base_api_url, user_data)
    assert create_response.status_code == 200

    delete_response = _delete_user(api_client, base_api_url, user_data)
    assert delete_response.status_code == 200

    payload = delete_response.json()
    assert payload["responseCode"] == 200
    assert "account deleted" in payload["message"].lower()


def test_api_update_user_account(api_client, base_api_url):
    user_data = _generate_test_user_data()
    create_response = _create_user(api_client, base_api_url, user_data)
    assert create_response.status_code == 200

    updated_data = user_data.copy()
    updated_data["company"] = "UpdatedCo"
    updated_data["name"] = "API Test Updated"

    update_response = api_client.put(
        f"{base_api_url}/updateAccount",
        data=updated_data,
    )
    assert update_response.status_code == 200
    assert update_response.json()["responseCode"] == 200

    get_response = api_client.get(
        f"{base_api_url}/getUserDetailByEmail",
        params={"email": user_data["email"]},
    )
    assert get_response.status_code == 200
    user = get_response.json()["user"]
    assert user["company"] == "UpdatedCo"

    delete_response = _delete_user(api_client, base_api_url, user_data)
    assert delete_response.status_code == 200


def test_api_get_user_detail_by_email(api_client, base_api_url):
    user_data = _generate_test_user_data()
    create_response = _create_user(api_client, base_api_url, user_data)
    assert create_response.status_code == 200

    get_response = api_client.get(
        f"{base_api_url}/getUserDetailByEmail",
        params={"email": user_data["email"]},
    )
    assert get_response.status_code == 200

    payload = get_response.json()
    assert payload["responseCode"] == 200
    assert payload["user"]["email"] == user_data["email"]

    delete_response = _delete_user(api_client, base_api_url, user_data)
    assert delete_response.status_code == 200
