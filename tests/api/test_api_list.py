def test_api_list_page(api_client):
    response = api_client.get("https://automationexercise.com/api_list")

    assert response.status_code == 200
    assert "Automation Practice for API Testing" in response.text
    assert "API Testing" in response.text
