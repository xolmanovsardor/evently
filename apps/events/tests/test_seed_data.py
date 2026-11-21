import pytest
from io import StringIO
from django.core.management import call_command
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.events.models import Event, EventStatus, EventType, Registration, RegistrationStatus
from apps.users.models import UserRole

User = get_user_model()


@pytest.mark.django_db
class TestSeedDataCommand:
    def test_seed_data_creates_all_expected_records(self):
        out = StringIO()
        call_command('seed_data', '--clear', stdout=out)
        output = out.getvalue()

        # Chiqish xabari tekshiruvi
        assert "Namunaviy ma'lumotlar muvaffaqiyatli yaratildi" in output

        # 1. Adminlar tekshiruvi (2 ta)
        admins = User.objects.filter(role=UserRole.ADMIN)
        assert admins.count() == 2
        admin_emails = list(admins.values_list('email', flat=True))
        assert "admin1@example.com" in admin_emails
        assert "admin2@example.com" in admin_emails

        for admin in admins:
            assert admin.is_superuser is True
            assert admin.is_staff is True
            assert admin.is_admin is True
            assert admin.check_password("AdminPassword123!") is True
            assert admin.telegram_chat_id is not None

        # 2. Oddiy foydalanuvchilar tekshiruvi (10 ta)
        users = User.objects.filter(role=UserRole.USER)
        assert users.count() == 10
        expected_user_emails = [f"user{i}@example.com" for i in range(1, 11)]
        user_emails = list(users.values_list('email', flat=True))
        for expected_email in expected_user_emails:
            assert expected_email in user_emails

        sample_user = User.objects.get(email="user1@example.com")
        assert sample_user.check_password("UserPassword123!") is True
        assert sample_user.first_name == "Jasur"
        assert sample_user.last_name == "Aliyev"
        assert sample_user.phone_number == "+998901234501"
        assert sample_user.telegram_chat_id == 200000001

        # 3. Tadbirlar tekshiruvi (15 ta)
        events = Event.objects.all()
        assert events.count() == 15

        now = timezone.now()

        # Kelajakdagi va o'tib ketgan tadbirlar
        upcoming_events = events.filter(start_at__gt=now)
        past_events = events.filter(end_at__lt=now)
        assert upcoming_events.count() > 0
        assert past_events.count() > 0

        # Ochiq va yopiq tadbirlar
        open_events = events.filter(status=EventStatus.OPEN)
        closed_events = events.filter(status=EventStatus.CLOSED)
        assert open_events.count() > 0
        assert closed_events.count() > 0

        # Barcha turlari mavjudligi
        seminars = events.filter(event_type=EventType.SEMINAR)
        masterclasses = events.filter(event_type=EventType.MASTERCLASS)
        trainings = events.filter(event_type=EventType.TRAINING)
        assert seminars.count() > 0
        assert masterclasses.count() > 0
        assert trainings.count() > 0

        # Cheksiz va cheklangan sig'imlar
        unlimited_events = events.filter(capacity__isnull=True)
        limited_events = events.filter(capacity__isnull=False)
        assert unlimited_events.count() > 0
        assert limited_events.count() > 0

        # 4. Ro'yxatdan o'tishlar va xususiyatlar
        registrations = Registration.objects.all()
        assert registrations.count() > 0

        active_regs = registrations.filter(status=RegistrationStatus.ACTIVE)
        cancelled_regs = registrations.filter(status=RegistrationStatus.CANCELLED)
        assert active_regs.count() > 0
        assert cancelled_regs.count() > 0

        # To'liq band qilingan tadbirni tekshirish
        full_event = Event.objects.get(title="To'liq Band Bo'lgan Tadbir (Sig'imi 3 kishi)")
        assert full_event.capacity == 3
        assert full_event.registered_count == 3
        assert full_event.available_seats == 0

    def test_seed_data_idempotency_without_clear(self):
        # 1-marta ishga tushirish
        call_command('seed_data')
        users_count_1 = User.objects.count()
        events_count_1 = Event.objects.count()
        regs_count_1 = Registration.objects.count()

        # 2-marta takroriy ishga tushirish (xatoliksiz va dublikatlarsiz o'tishi kerak)
        out = StringIO()
        call_command('seed_data', stdout=out)
        assert "Namunaviy ma'lumotlar muvaffaqiyatli yaratildi" in out.getvalue()

        assert User.objects.count() == users_count_1
        assert Event.objects.count() == events_count_1
        assert Registration.objects.count() == regs_count_1

    def test_seed_data_clear_option(self):
        call_command('seed_data')
        assert Event.objects.count() == 15

        out = StringIO()
        call_command('seed_data', '--clear', stdout=out)
        output = out.getvalue()
        assert "Mavjud seed ma'lumotlar tozalanmoqda" in output
        assert "Tozalandi:" in output
        assert Event.objects.count() == 15
