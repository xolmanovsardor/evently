import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.users.models import UserRole
from apps.events.models import Event, EventType, EventStatus, Registration, RegistrationStatus

logger = logging.getLogger('django')
User = get_user_model()


class Command(BaseCommand):
    help = "Namunaviy ma'lumotlar yaratish (Seed Data): 2 admin, 10 oddiy user, 15 ta turli xil tadbirlar va ro'yxatdan o'tishlar."

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Avval yaratilgan seed ma'lumotlarni tozalab, keyin yangidan yaratish.",
        )

    def handle(self, *args, **options):
        clear_first = options.get('clear', False)

        self.stdout.write(self.style.MIGRATE_HEADING("=== Evently Seed Data Generator ==="))

        with transaction.atomic():
            if clear_first:
                self._clear_seed_data()

            admins = self._create_admins()
            users = self._create_users()
            events = self._create_events(admins)
            self._create_registrations(users, events)

        self.stdout.write(self.style.SUCCESS("=== Namunaviy ma'lumotlar muvaffaqiyatli yaratildi! ==="))

    def _clear_seed_data(self):
        self.stdout.write("Mavjud seed ma'lumotlar tozalanmoqda...")
        emails = [
            'admin1@example.com',
            'admin2@example.com',
        ] + [f"user{i}@example.com" for i in range(1, 11)]

        # Foydalanuvchilar o'chirilganda, CASCADE sababli Registration va bog'liq modellar ham tozalanadi
        deleted_users, _ = User.objects.filter(email__in=emails).delete()

        # Seed tadbirlarni tozalash (yaratuvchi bo'yicha yoki seed nomlari bilan)
        seed_titles = [
            "Python & Django Backend Me'morchiligi",
            "aiogram 3.x bilan Mukammal Telegram Botlar",
            "PostgreSQL Optimallashtirish va Indekslar",
            "Docker va Kubernetes: Mikroservislar Asosi",
            "Sun'iy Intellekt va LLM larni Loyihalarga Integratsiya Qilish",
            "REST API Xavfsizligi va JWT Eng Yaxshi Amaliyotlar",
            "Frontend va Backend Integratsiyasi: React + DRF",
            "Eslatmalar va Bildirishnomalar Dvigateli (24 Soat Qolgan Tadbir)",
            "To'liq Band Bo'lgan Tadbir (Sig'imi 3 kishi)",
            "Yopiq Tadbir: Korporativ Backend Audit",
            "Muddatidan Oldin Yopilgan Master-klass",
            "O'tib Ketgan Tadbir: Django 5.0 Yangiliklari",
            "O'tib Ketgan Tadbir: Async Python va FastAPI",
            "O'tib Ketgan Yopiq Tadbir: Kiberxavfsizlik Konferensiyasi 2025",
            "Cheksiz Sig'imli Katta Ochiq Hackathon 2026",
        ]
        deleted_events, _ = Event.objects.filter(title__in=seed_titles).delete()
        self.stdout.write(
            self.style.WARNING(f"Tozalandi: {deleted_users} ta foydalanuvchi, {deleted_events} ta tadbir.")
        )

    def _create_admins(self) -> list[User]:
        self.stdout.write("Admin hisoblari yaratilmoqda...")
        admins_data = [
            {
                "email": "admin1@example.com",
                "first_name": "Aziz",
                "last_name": "Rahimov",
                "phone_number": "+998901111111",
                "telegram_chat_id": 100000001,
            },
            {
                "email": "admin2@example.com",
                "first_name": "Malika",
                "last_name": "Karimova",
                "phone_number": "+998902222222",
                "telegram_chat_id": 100000002,
            },
        ]

        admins = []
        for data in admins_data:
            email = data["email"]
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create_superuser(
                    email=email,
                    password="AdminPassword123!",
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    phone_number=data["phone_number"],
                    role=UserRole.ADMIN,
                    telegram_chat_id=data["telegram_chat_id"],
                )
                self.stdout.write(self.style.SUCCESS(f"  + Admin yaratildi: {email}"))
            else:
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                user.phone_number = data["phone_number"]
                user.telegram_chat_id = data["telegram_chat_id"]
                user.role = UserRole.ADMIN
                user.is_staff = True
                user.is_superuser = True
                user.set_password("AdminPassword123!")
                user.save()
                self.stdout.write(f"  * Admin mavjud (yangilandi): {email}")
            admins.append(user)

        return admins

    def _create_users(self) -> list[User]:
        self.stdout.write("Oddiy foydalanuvchi hisoblari yaratilmoqda (10 ta)...")
        users_info = [
            ("user1@example.com", "Jasur", "Aliyev", "+998901234501", 200000001),
            ("user2@example.com", "Nigora", "Sobirova", "+998901234502", 200000002),
            ("user3@example.com", "Bobur", "Mirzayev", "+998901234503", 200000003),
            ("user4@example.com", "Shahzoda", "Yo'ldosheva", "+998901234504", None),
            ("user5@example.com", "Dilshod", "Qodirov", "+998901234505", 200000005),
            ("user6@example.com", "Gulnoza", "Umarova", "+998901234506", None),
            ("user7@example.com", "Farrux", "Toshmatov", "+998901234507", 200000007),
            ("user8@example.com", "Kamola", "Bekmirzayeva", "+998901234508", None),
            ("user9@example.com", "Otabek", "Shokirov", "+998901234509", 200000009),
            ("user10@example.com", "Ziyoda", "Saidova", "+998901234510", None),
        ]

        users = []
        for email, first, last, phone, tg_id in users_info:
            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create_user(
                    email=email,
                    password="UserPassword123!",
                    first_name=first,
                    last_name=last,
                    phone_number=phone,
                    role=UserRole.USER,
                    telegram_chat_id=tg_id,
                )
                self.stdout.write(self.style.SUCCESS(f"  + Foydalanuvchi yaratildi: {email}"))
            else:
                user.first_name = first
                user.last_name = last
                user.phone_number = phone
                user.telegram_chat_id = tg_id
                user.role = UserRole.USER
                user.set_password("UserPassword123!")
                user.save()
                self.stdout.write(f"  * Foydalanuvchi mavjud (yangilandi): {email}")
            users.append(user)

        return users

    def _create_events(self, admins: list[User]) -> list[Event]:
        self.stdout.write("15 ta namunaviy tadbir yaratilmoqda...")
        now = timezone.now()
        admin1, admin2 = admins[0], admins[1]

        events_specs = [
            # 1. Kelajakdagi ochiq, cheklangan sig'imli
            {
                "title": "Python & Django Backend Me'morchiligi",
                "description": "Django 5.1, DRF va arxitektura tamoyillari bo'yicha chuqurlashtirilgan seminar.",
                "event_type": EventType.SEMINAR,
                "location": "Toshkent, IT Park binosi, 301-xona",
                "start_at": now + timedelta(days=2),
                "end_at": now + timedelta(days=2, hours=3),
                "capacity": 30,
                "status": EventStatus.OPEN,
                "created_by": admin1,
            },
            # 2. Masterclass, katta sig'imli
            {
                "title": "aiogram 3.x bilan Mukammal Telegram Botlar",
                "description": "Asinxron arxitektura, Routers, FSM va webhooklar bilan ishlash master-klassi.",
                "event_type": EventType.MASTERCLASS,
                "location": "Onlayn (Zoom / YouTube Live)",
                "start_at": now + timedelta(days=5),
                "end_at": now + timedelta(days=5, hours=2),
                "capacity": 100,
                "status": EventStatus.OPEN,
                "created_by": admin1,
            },
            # 3. Training
            {
                "title": "PostgreSQL Optimallashtirish va Indekslar",
                "description": "So'rovlarni tezlashtirish, EXPLAIN ANALYZE va indeks turlari bo'yicha amaliy trening.",
                "event_type": EventType.TRAINING,
                "location": "Toshkent, C-Space Coworking Yunusobod",
                "start_at": now + timedelta(days=7),
                "end_at": now + timedelta(days=7, hours=4),
                "capacity": 25,
                "status": EventStatus.OPEN,
                "created_by": admin2,
            },
            # 4. Docker & K8s
            {
                "title": "Docker va Kubernetes: Mikroservislar Asosi",
                "description": "Konteynerlashtirish va klasterlarni boshqarishga bag'ishlangan nazariy va amaliy seminar.",
                "event_type": EventType.SEMINAR,
                "location": "Toshkent, GroundZero Chilanzar",
                "start_at": now + timedelta(days=10),
                "end_at": now + timedelta(days=10, hours=3),
                "capacity": 50,
                "status": EventStatus.OPEN,
                "created_by": admin2,
            },
            # 5. Cheksiz sig'imli (capacity=None)
            {
                "title": "Sun'iy Intellekt va LLM larni Loyihalarga Integratsiya Qilish",
                "description": "Katta til modellari va API lar bilan samarali ishlash bo'yicha ochiq master-klass.",
                "event_type": EventType.MASTERCLASS,
                "location": "Onlayn (Google Meet)",
                "start_at": now + timedelta(days=12),
                "end_at": now + timedelta(days=12, hours=2),
                "capacity": None,
                "status": EventStatus.OPEN,
                "created_by": admin1,
            },
            # 6. REST API Security
            {
                "title": "REST API Xavfsizligi va JWT Eng Yaxshi Amaliyotlar",
                "description": "Xavfsiz autentifikatsiya, brute-force himoyasi va token boshqaruvi.",
                "event_type": EventType.SEMINAR,
                "location": "Toshkent, UEnter Innovatsiya Markazi",
                "start_at": now + timedelta(days=14),
                "end_at": now + timedelta(days=14, hours=3),
                "capacity": 40,
                "status": EventStatus.OPEN,
                "created_by": admin1,
            },
            # 7. Frontend + Backend
            {
                "title": "Frontend va Backend Integratsiyasi: React + DRF",
                "description": "To'liq sikldagi veb-ilovalarni birgalikda ishlab chiqish amaliyoti.",
                "event_type": EventType.TRAINING,
                "location": "Samarqand, IT Park filiali",
                "start_at": now + timedelta(days=18),
                "end_at": now + timedelta(days=18, hours=5),
                "capacity": 20,
                "status": EventStatus.OPEN,
                "created_by": admin2,
            },
            # 8. 24 soatdan kam vaqt qolgan tadbir (eslatmalar uchun ideal)
            {
                "title": "Eslatmalar va Bildirishnomalar Dvigateli (24 Soat Qolgan Tadbir)",
                "description": "Avtomatik eslatmalar mexanizmini tekshirish uchun maxsus tadbir.",
                "event_type": EventType.SEMINAR,
                "location": "Onlayn vebinar",
                "start_at": now + timedelta(hours=18),
                "end_at": now + timedelta(hours=20),
                "capacity": 15,
                "status": EventStatus.OPEN,
                "created_by": admin1,
            },
            # 9. Kichik sig'imli (to'ldiriladigan tadbir)
            {
                "title": "To'liq Band Bo'lgan Tadbir (Sig'imi 3 kishi)",
                "description": "Maksimal sig'im qoidasi va race-condition holatlarini ko'rish uchun test tadbiri.",
                "event_type": EventType.MASTERCLASS,
                "location": "Toshkent, Coworking xona 12",
                "start_at": now + timedelta(days=3),
                "end_at": now + timedelta(days=3, hours=2),
                "capacity": 3,
                "status": EventStatus.OPEN,
                "created_by": admin1,
            },
            # 10. Yopiq holatdagi kelajakdagi tadbir
            {
                "title": "Yopiq Tadbir: Korporativ Backend Audit",
                "description": "Faqat taklif etilgan tashkilotlar uchun maxsus yopiq trening.",
                "event_type": EventType.TRAINING,
                "location": "Toshkent, Markaziy Bank Binosi",
                "start_at": now + timedelta(days=4),
                "end_at": now + timedelta(days=4, hours=4),
                "capacity": 10,
                "status": EventStatus.CLOSED,
                "created_by": admin2,
            },
            # 11. Muddatidan oldin yopilgan
            {
                "title": "Muddatidan Oldin Yopilgan Master-klass",
                "description": "Tashkilotchi tomonidan ro'yxatdan o'tish to'xtatilgan tadbir.",
                "event_type": EventType.MASTERCLASS,
                "location": "Onlayn",
                "start_at": now + timedelta(days=8),
                "end_at": now + timedelta(days=8, hours=2),
                "capacity": 50,
                "status": EventStatus.CLOSED,
                "created_by": admin1,
            },
            # 12. O'tib ketgan ochiq tadbir
            {
                "title": "O'tib Ketgan Tadbir: Django 5.0 Yangiliklari",
                "description": "O'tgan oyda muvaffaqiyatli yakunlangan taqdimot va seminar.",
                "event_type": EventType.SEMINAR,
                "location": "Toshkent, INHA Universiteti",
                "start_at": now - timedelta(days=10),
                "end_at": now - timedelta(days=10, hours=-3),
                "capacity": 60,
                "status": EventStatus.OPEN,
                "created_by": admin1,
            },
            # 13. O'tib ketgan training
            {
                "title": "O'tib Ketgan Tadbir: Async Python va FastAPI",
                "description": "O'tgan hafta bo'lib o'tgan asinxron dasturlash asoslari treningi.",
                "event_type": EventType.TRAINING,
                "location": "Toshkent, TUIT binosi",
                "start_at": now - timedelta(days=5),
                "end_at": now - timedelta(days=5, hours=-4),
                "capacity": 35,
                "status": EventStatus.OPEN,
                "created_by": admin2,
            },
            # 14. O'tib ketgan yopiq tadbir
            {
                "title": "O'tib Ketgan Yopiq Tadbir: Kiberxavfsizlik Konferensiyasi 2025",
                "description": "O'tgan yili o'tkazilgan yillik xavfsizlik forumi.",
                "event_type": EventType.SEMINAR,
                "location": "Toshkent, Hyatt Regency",
                "start_at": now - timedelta(days=30),
                "end_at": now - timedelta(days=30, hours=-6),
                "capacity": 200,
                "status": EventStatus.CLOSED,
                "created_by": admin1,
            },
            # 15. Cheksiz sig'imli kelajakdagi ochiq tadbir
            {
                "title": "Cheksiz Sig'imli Katta Ochiq Hackathon 2026",
                "description": "Barcha yosh dasturchilar uchun 48 soatlik ochiq hakaton.",
                "event_type": EventType.TRAINING,
                "location": "Toshkent, Yoshlar Ijod Saroyi",
                "start_at": now + timedelta(days=25),
                "end_at": now + timedelta(days=27),
                "capacity": None,
                "status": EventStatus.OPEN,
                "created_by": admin2,
            },
        ]

        events = []
        for spec in events_specs:
            event, created = Event.objects.get_or_create(
                title=spec["title"],
                defaults=spec,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"  + Tadbir yaratildi: {event.title}"))
            else:
                for k, v in spec.items():
                    setattr(event, k, v)
                event.save()
                self.stdout.write(f"  * Tadbir mavjud (yangilandi): {event.title}")
            events.append(event)

        return events

    def _create_registrations(self, users: list[User], events: list[Event]):
        self.stdout.write("Namunaviy ro'yxatdan o'tishlar kiritilmoqda...")
        now = timezone.now()

        # Tadbir 9 ("To'liq Band Bo'lgan Tadbir", capacity=3): user1, user2, user3
        full_event = events[8]
        for u in users[:3]:
            Registration.objects.update_or_create(
                user=u,
                event=full_event,
                defaults={"status": RegistrationStatus.ACTIVE, "reminder_sent": False},
            )

        # Tadbir 8 (18 soat qolgan): user1, user2, user5
        reminder_event = events[7]
        for u in [users[0], users[1], users[4]]:
            Registration.objects.update_or_create(
                user=u,
                event=reminder_event,
                defaults={"status": RegistrationStatus.ACTIVE, "reminder_sent": False},
            )

        # Tadbir 1: user1, user4, user6, user7
        first_event = events[0]
        for u in [users[0], users[3], users[5], users[6]]:
            Registration.objects.update_or_create(
                user=u,
                event=first_event,
                defaults={"status": RegistrationStatus.ACTIVE, "reminder_sent": False},
            )

        # Bitta bekor qilingan ro'yxatdan o'tish (Cancelled test uchun): user8 -> first_event
        Registration.objects.update_or_create(
            user=users[7],
            event=first_event,
            defaults={
                "status": RegistrationStatus.CANCELLED,
                "cancelled_at": now,
                "reminder_sent": False,
            },
        )

        # O'tib ketgan tadbirga ro'yxatdan o'tganlar: Tadbir 12
        past_event = events[11]
        for u in users[:4]:
            Registration.objects.update_or_create(
                user=u,
                event=past_event,
                defaults={"status": RegistrationStatus.ACTIVE, "reminder_sent": True},
            )

        total_regs = Registration.objects.count()
        self.stdout.write(self.style.SUCCESS(f"  + Ro'yxatdan o'tishlar saqlandi (Jami: {total_regs} ta)"))
