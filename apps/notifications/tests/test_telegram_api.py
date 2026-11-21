import pytest
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email="testuser@example.com",
        password="Password123!",
        first_name="Test",
        last_name="User"
    )


@pytest.mark.django_db
class TestTelegramLinkAPI:
    def test_telegram_link_unauthenticated(self, api_client):
        response = api_client.post('/api/v1/telegram/link/')
        assert response.status_code == 401

    def test_telegram_link_success(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        response = api_client.post('/api/v1/telegram/link/')
        assert response.status_code == 200
        data = response.data
        assert 'link' in data
        assert 'token' in data
        assert f"t.me/{settings.TELEGRAM_BOT_USERNAME}?start=" in data['link']

        regular_user.refresh_from_db()
        assert regular_user.telegram_link_token == data['token']


@pytest.mark.django_db
class TestTelegramConfirmAPI:
    def test_telegram_confirm_wrong_secret(self, api_client, regular_user):
        regular_user.telegram_link_token = "valid-token-123"
        regular_user.save()

        response = api_client.post(
            '/api/v1/telegram/confirm/',
            data={"token": "valid-token-123", "chat_id": 998877},
            HTTP_X_BOT_SECRET="wrong-secret-key"
        )
        assert response.status_code == 403
        assert response.data['detail'] == "Noto'g'ri maxfiy kalit."

    def test_telegram_confirm_invalid_token(self, api_client):
        response = api_client.post(
            '/api/v1/telegram/confirm/',
            data={"token": "non-existent-token", "chat_id": 998877},
            HTTP_X_BOT_SECRET=settings.BOT_API_SECRET
        )
        assert response.status_code == 400
        assert "Yaroqsiz" in response.data['detail']

    def test_telegram_confirm_success(self, api_client, regular_user):
        regular_user.telegram_link_token = "valid-token-xyz"
        regular_user.save()

        response = api_client.post(
            '/api/v1/telegram/confirm/',
            data={"token": "valid-token-xyz", "chat_id": 123456789},
            HTTP_X_BOT_SECRET=settings.BOT_API_SECRET
        )
        assert response.status_code == 200
        assert response.data['email'] == regular_user.email

        regular_user.refresh_from_db()
        assert regular_user.telegram_chat_id == 123456789
        assert regular_user.telegram_link_token is None
