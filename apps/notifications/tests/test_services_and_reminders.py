from datetime import timedelta
from unittest.mock import patch
import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient

from apps.events.models import Event, EventStatus, Registration, RegistrationStatus
from apps.events.services import register_for_event

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def users_fixture(db):
    user = User.objects.create_user(
        email="participant@example.com",
        password="Password123!",
        first_name="Ali",
        last_name="Valiyev",
        phone_number="+998901234567",
        telegram_chat_id=111111
    )
    admin = User.objects.create_superuser(
        email="admin@example.com",
        password="AdminPassword123!",
        first_name="Admin",
        last_name="Boshliq",
        telegram_chat_id=999999
    )
    return user, admin


@pytest.fixture
def upcoming_event(db):
    now = timezone.now()
    return Event.objects.create(
        title="Django & AI Seminar",
        description="Qiziqarli seminar",
        event_type="seminar",
        location="Tashkent",
        start_at=now + timedelta(hours=10),
        end_at=now + timedelta(hours=12),
        capacity=50,
        status=EventStatus.OPEN
    )


@pytest.mark.django_db
class TestNotificationServicesAndReminders:
    def test_telegram_send_failure_does_not_break_registration(self, users_fixture, upcoming_event):
        user, _ = users_fixture

        with patch('apps.notifications.services.requests.post', side_effect=Exception("Network error")):
            # Ro'yxatdan o'tish Telegram ishlamasa ham xatosiz o'tishi kerak
            reg = register_for_event(user, upcoming_event)
            assert reg.id is not None
            assert reg.status == RegistrationStatus.ACTIVE

    @pytest.mark.django_db(transaction=True)
    def test_registration_triggers_user_and_admin_notifications(self, users_fixture, upcoming_event):
        user, admin = users_fixture

        with patch('apps.notifications.services.send_telegram_message', return_value=True) as mock_send:
            reg = register_for_event(user, upcoming_event)
            assert reg.status == RegistrationStatus.ACTIVE

            # Foydalanuvchi va admin uchun send_telegram_message chaqirilishi kerak
            assert mock_send.call_count >= 2
            called_chat_ids = [call.args[0] for call in mock_send.call_args_list]
            assert user.telegram_chat_id in called_chat_ids
            assert admin.telegram_chat_id in called_chat_ids

    def test_reminder_command_only_sent_once(self, users_fixture, upcoming_event):
        user, _ = users_fixture

        reg = Registration.objects.create(
            user=user,
            event=upcoming_event,
            status=RegistrationStatus.ACTIVE,
            reminder_sent=False
        )

        with patch('apps.notifications.services.send_telegram_message', return_value=True) as mock_send:
            # 1-marta ishga tushirish: eslatma yuborilishi kerak
            call_command('send_event_reminders', hours=24)
            assert mock_send.call_count == 1
            reg.refresh_from_db()
            assert reg.reminder_sent is True

            # 2-marta qayta ishga tushirish: qayta yuborilmasligi kerak!
            mock_send.reset_mock()
            call_command('send_event_reminders', hours=24)
            assert mock_send.call_count == 0
