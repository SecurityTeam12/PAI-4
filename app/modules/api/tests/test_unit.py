import pytest

from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from app.modules.api.services import APITokenService
api_service = APITokenService()


@pytest.fixture(scope='module')
def test_client_with_token(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()

        token, error = api_service.generate_token(user_id=user_test.id, user_email=user_test.email, expiration_days=10)
        assert token is not None, f"Token generation failed with error: {error}"

    yield test_client, token


def test_token_generation_valid():
    """
    Tests that API token generation works.
    """
    token, error = api_service.generate_token(1, 'user@example.com', 10)

    assert token is not None, "Token generation does not work properly."
    assert error is None, "An error occurred while generating the token."


def test_token_generation_invalid_negative():
    """
    Tests that API token generation does not work for a negative value for days.
    """
    token, error = api_service.generate_token(1, 'user@example.com', -10)

    assert token is None, "Token generation does not work properly."
    assert isinstance(error, ValueError), "Expected ValueError, but received a different error."


def test_api_configuration_page_get(test_client_with_token):
    """
    Tests access to the API configuration page via a GET request.
    """
    test_client, token = test_client_with_token

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/api/configuration")
    assert response.status_code == 200, "The API configuration page could not be accessed."
    assert b"Generate New API Token" in response.data, "The expected content is not present on the page"

    logout(test_client)


def test_api_configuration_page_post(test_client_with_token):
    """
    Tests token generation via a POST request.
    """
    test_client, token = test_client_with_token

    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = test_client.post("/api/configuration", data={"expiration": "30"}, headers=headers)
    assert response.status_code == 200, "POST request failed on /api/configuration."
    assert b"API token generated successfully" in response.data, "Token was not generated as expected."

    logout(test_client)


def test_api_dataset_list_unauthorized(test_client_with_token):
    """
    Tests access to the API dataset list page via a GET request without authentication.
    Expects a 401 Unauthorized status code.
    """
    test_client, token = test_client_with_token

    response = test_client.get("/api/dataset/list")
    assert response.status_code == 401, "Expected 401 Unauthorized, but received a different status code."


def test_api_dataset_list_authorized(test_client_with_token):
    """
    Tests access to the API dataset list page with authentication.
    """
    test_client, token = test_client_with_token

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = test_client.get("/api/dataset/list", headers=headers)
    assert response.status_code == 200, "Failed to access /api/dataset/list with valid credentials and token."
    assert b"My datasets" in response.data, "Expected dataset list content not found."

    logout(test_client)


def test_api_dataset_upload_get(test_client_with_token):
    """
    Tests access to the dataset upload page via a GET request.
    """
    test_client, token = test_client_with_token

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = test_client.get("/api/dataset/upload", headers=headers)
    assert response.status_code == 200, "Failed to access /api/dataset/upload with GET request."
    assert b"Upload dataset" in response.data, "Expected upload dataset content not found."

    logout(test_client)


def test_api_profile_edit_get(test_client_with_token):
    """
    Tests access to the profile edit page via a GET request.
    """
    test_client, token = test_client_with_token

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = test_client.get("/api/profile/edit", headers=headers)
    assert response.status_code == 200, "Failed to access profile edit page with GET request."
    assert b"Edit profile" in response.data, "Expected profile edit content not found."


def test_api_profile_summary_get(test_client_with_token):
    """
    Tests access to the profile summary page via a GET request.
    """
    test_client, token = test_client_with_token

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = test_client.get("/api/profile/summary", headers=headers)
    assert response.status_code == 200, "Failed to access profile summary page with GET request."
    assert b"User profile" in response.data, "Expected profile summary content not found."
