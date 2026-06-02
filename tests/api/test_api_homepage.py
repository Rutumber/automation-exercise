def test_api_homepage_status(api_client):
    response = api_client.get("https://automationexercise.com")

    assert response.status_code == 200
    assert "Automation Exercise" in response.text
