# Evently — Loyihani Bosqichma-bosqich Amalga Oshirish Rejasi (Event Plan)

> **Loyiha:** Evently — Tadbirlarni boshqarish platformasi (Backend REST API + Telegram Bot)  
> **Texnologiyalar:** Python 3.11+, Django 5.1, DRF, SimpleJWT, drf-spectacular, PostgreSQL, aiogram 3.x, pytest-django  
> **Hujjat maqsadi:** Loyihadagi barcha ishlarni katta bosqichlarga va ularning tarkibiy qismlariga ajratish hamda bajarilgan (`[x]`) va bajarilmagan (`[ ]`) qismlarni nazorat qilib borish.

---

## Umumiy Holat Paneli (Progress Summary)

| # | Katta Bosqich Nomi | Holati | Testlar |
| :---: | :--- | :---: | :---: |
| **1** | [Muhit, Infratuzilma va Multi-Agent Tizimi](#1-bosqich-muhit-infratuzilma-va-multi-agent-tizimi) | ✅ Bajarildi | - |
| **2** | [Django Core & Settings Me'morchiligi](#2-bosqich-django-core--settings-memorchiligi) | ✅ Bajarildi | 5 / 5 |
| **3** | [Foydalanuvchilar, Autentifikatsiya va Ruxsatlar (Auth)](#3-bosqich-foydalanuvchilar-autentifikatsiya-va-ruxsatlar-auth) | ✅ Bajarildi | 12 / 12 |
| **4** | [Tadbirlar Boshqaruvi va Filtrlash (Events CRUD)](#4-bosqich-tadbirlar-boshqaruvi-va-filtrlash-events-crud) | ✅ Bajarildi | 12 / 12 |
| **5** | [Ro'yxatdan O'tish va Biznes Qoidalar (Registration)](#5-bosqich-royxatdan-otish-va-biznes-qoidalar-registration) | ✅ Bajarildi | 13 / 13 |
| **6** | [Telegram Bot Integratsiyasi va Xabarnomalar](#6-bosqich-telegram-bot-integratsiyasi-va-xabarnomalar) | ✅ Bajarildi | 5 / 5 |
| **7** | [Avtomatik Eslatmalar Mexanizmi (Reminders)](#7-bosqich-avtomatik-eslatmalar-mexanizmi-reminders) | ✅ Bajarildi | 3 / 3 |
| **8** | [Alohida aiogram 3.x Telegram Bot Dasturi](#8-bosqich-alohida-aiogram-3x-telegram-bot-dasturi) | ❌ Kutilmoqda | - |
| **9** | [Namunaviy Ma'lumotlar Yaratish (Seed Data)](#9-bosqich-namunaviy-malumotlar-yaratish-seed-data) | ❌ Kutilmoqda | - |
| **10** | [Sifat Nazorati va To'liq Integratsion Testlar](#10-bosqich-sifat-nazorati-va-toliq-integratsion-testlar) | ⏳ Qisman (50/50 PASS) | 50 / 50 |
| **11** | [Production Deployment va Yakuniy Topshirish](#11-bosqich-production-deployment-va-yakuniy-topshirish) | ❌ Kutilmoqda | - |

---

## 1-BOSQICH: Muhit, Infratuzilma va Multi-Agent Tizimi
*Loyiha poydevori, kutubxonalar, versiyalar boshqaruvi va AI agentlar dvigateli.*

- [x] **Virtual muhit va kutubxonalar:**
  - [x] Python 3.11+ virtualenv yaratildi.
  - [x] `requirements.txt` tayyorlandi va barcha kutubxonalar o'rnatildi (Django 5.1, DRF, SimpleJWT, drf-spectacular, psycopg, django-filter, django-cors-headers, pytest-django, aiogram).
- [x] **Konfiguratsiya fayllari:**
  - [x] `.env.example` — namunaviy konfiguratsiya.
  - [x] `.env` — lokal muhit sozlamalari (`.gitignore` da himoyalangan).
  - [x] `pytest.ini` — Django test runner sozlamalari.
  - [x] `.gitignore` — nozik va ortiqcha fayllar cheklandi.
- [x] **Multi-Agent Tizimi (`.agents/`):**
  - [x] `AGENTS.md` — qat'iy Git-Flow va agentlar boshqaruv qoidalari.
  - [x] `workflow.py` — Orchestrator CLI boshqaruv dvigateli (`start`, `test`, `review`, `finish`, `abort`).
  - [x] `state.json` — jarayon holatini doimiy qayd etish.
  - [x] 4 ta ixtisoslashgan agent o'rnatildi: `orchestrator`, `architect`, `engineer`, `reviewer`.

---

## 2-BOSQICH: Django Core & Settings Me'morchiligi
*Loyiha yadrosi, xatoliklarni qayta ishlash, sahifalash, loglar va hujjatlashtirish.*

- [x] **Django loyiha tuzilmasi (`config/`):**
  - [x] `manage.py`, `config/settings.py`, `config/urls.py`, `config/asgi.py`, `config/wsgi.py`.
- [x] **Xatoliklar boshqaruvi ([config/exceptions.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/config/exceptions.py)):
  - [x] `BusinessLogicError` klassi yaratildi.
  - [x] Biznes xatolar yagona formatga keltirildi: `{ "detail": "...", "code": "..." }`.
  - [x] `custom_exception_handler` DRF sozlamalariga ulandi.
- [x] **Standartlashtirilgan Sahifalash ([config/pagination.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/config/pagination.py)):
  - [x] `CustomPagination` joriy qilindi (`page_size=10`, `max_page_size=100`, `page_size_query_param='page_size'`).
  - [x] Chiqish formati: `count`, `total_pages`, `current_page`, `page_size`, `next`, `previous`, `results`.
- [x] **Logging tizimi ([config/settings.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/config/settings.py)):
  - [x] `logs/` katalogi sozlandi.
  - [x] `logs/django.log`, `logs/errors.log`, `logs/telegram.log` fayllariga log yozish yoqildi.
- [x] **Health Check Endpoint ([config/views.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/config/views.py)):
  - [x] `GET /api/v1/health/` — server, baza ulanishi va vaqt mintaqasi holatini tekshirish.
- [x] **Swagger va OpenAPI 3 hujjatlashtirish:**
  - [x] `GET /api/schema/` — OpenAPI JSON/YAML schema.
  - [x] `GET /api/docs/` — Swagger UI interfeysi.
  - [x] `GET /api/redoc/` — Redoc interfeysi.
- [x] **CORS va Media sozlamalari:**
  - [x] `django-cors-headers` middleware va ochiq originlar ulandi.
  - [x] `MEDIA_URL` va `MEDIA_ROOT` sozlandi.

---

## 3-BOSQICH: Foydalanuvchilar, Autentifikatsiya va Ruxsatlar (Auth)
*Foydalanuvchi modeli, JWT tokenlar, xavfsizlik va profil boshqaruvi.*

- [x] **Custom User Modeli ([apps/users/models.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/users/models.py)):
  - [x] `AbstractUser` asosidagi model: `email` (asosiy identifikator, unikal).
  - [x] Maydonlar: `first_name`, `last_name`, `phone_number`, `role` (`admin`/`user`), `telegram_chat_id`, `telegram_link_token`.
  - [x] Propertilar: `is_admin`, `full_name`.
- [x] **User Manager ([apps/users/managers.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/users/managers.py)):
  - [x] `create_user(email, password, ...)` — oddiy foydalanuvchi yaratish (`role='user'`).
  - [x] `create_superuser(email, password, ...)` — superuser yaratish (`role='admin'`, `is_staff=True`, `is_superuser=True`).
- [x] **Ruxsatlar ([apps/users/permissions.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/users/permissions.py)):
  - [x] `IsAdmin` — faqat admin foydalanuvchilar uchun.
  - [x] `IsAdminOrReadOnly` — xavfsiz metodlar hammaga, qolgani faqat adminga.
- [x] **Autentifikatsiya API ([apps/users/views.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/users/views.py)):
  - [x] `POST /api/v1/auth/register/` — ro'yxatdan o'tish (parol tasdiqlash, telefon raqami formati `+998...`).
  - [x] *Xavfsizlik qoidasi:* API orqali `role='admin'` yuborilsa ham foydalanuvchi `user` bo'lib qoladi.
  - [x] `POST /api/v1/auth/login/` — SimpleJWT orqali `access` va `refresh` token olish.
  - [x] `POST /api/v1/auth/token/refresh/` — tokenni yangilash.
  - [x] `GET /api/v1/auth/me/` — o'z profilini ko'rish (faqat login qilganlar).
  - [x] `PATCH /api/v1/auth/me/` — profilni tahrirlash (rol va email o'zgartirilmaydi).
- [x] **Django Admin integratsiyasi ([apps/users/admin.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/users/admin.py)):
  - [x] `UserAdmin` orqali admin paneldan boshqarish.

---

## 4-BOSQICH: Tadbirlar Boshqaruvi va Filtrlash (Events CRUD)
*Tadbirlar yaratish, tahrirlash, o'chirish, qidiruv, saralash va biznes cheklovlari.*

- [x] **Event Modeli ([apps/events/models.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/events/models.py)):
  - [x] Maydonlar: `title`, `description`, `event_type` (`seminar`, `masterclass`, `training`), `location`, `start_at`, `end_at`, `capacity` (null = cheksiz), `status` (`open`, `closed`), `created_by`, `created_at`, `updated_at`.
  - [x] Propertilar: `registered_count`, `available_seats`, `is_finished`.
- [x] **Tadbirlar API ([apps/events/views.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/events/views.py)):
  - [x] `GET /api/v1/events/` — tadbirlar ro'yxati (ochiq API, pagination bilan).
  - [x] `GET /api/v1/events/{id}/` — tadbir haqida batafsil (ochiq API).
  - [x] `POST /api/v1/events/` — tadbir yaratish (**BR-4**: faqat admin, oddiy userga `403`, mehmonga `401`).
  - [x] `PATCH /api/v1/events/{id}/` — tadbirni tahrirlash (faqat admin).
  - [x] `DELETE /api/v1/events/{id}/` — tadbirni o'chirish (faqat admin).
  - [x] `POST /api/v1/events/{id}/close/` — tadbirni muddatidan oldin yopish (faqat admin).
- [x] **Biznes Validatsiyalar ([apps/events/serializers.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/events/serializers.py)):
  - [x] **BR-7:** `end_at` har doim `start_at` dan keyin bo'lishi shart.
  - [x] **BR-8:** Yangi tadbir yaratishda `start_at` o'tgan sanaga qo'yilishi taqiqlanadi.
  - [x] **BR-9:** `capacity` ni mavjud faol qatnashuvchilar sonidan kamaytirib bo'lmaydi (`code: capacity_too_low`).
  - [x] `status` va `created_by` maydonlari oddiy patch orqali o'zgarmaydi (`read_only`).
- [x] **Filtrlash va Qidiruv ([apps/events/filters.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/events/filters.py)):
  - [x] `?event_type=seminar` bo'yicha filter.
  - [x] `?status=open` bo'yicha filter.
  - [x] `?upcoming=true` faqat kelajakdagi tadbirlarni ko'rsatish.
  - [x] `?search=django` (`title` va `description` bo'yicha qidiruv).
  - [x] `?ordering=start_at` / `-start_at` bo'yicha saralash.
- [x] **Django Admin integratsiyasi ([apps/events/admin.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/events/admin.py)):
  - [x] `EventAdmin` filtrlash va qidiruv bilan ulandi.

---

## 5-BOSQICH: Ro'yxatdan O'tish va Biznes Qoidalar (Registration)
*Tadbirga yozilish, chiqish, joylarni nazorat qilish va race condition himoyasi.*

- [x] **Registration Modeli:**
  - [x] `user` (ForeignKey User), `event` (ForeignKey Event), `status` (`active` / `cancelled`), `reminder_sent` (bool), `created_at`, `cancelled_at`.
  - [x] **Majburiy Constraint:** `UniqueConstraint(fields=['user', 'event'], name='unique_user_event_registration')`.
- [x] **Tadbirga yozilish xizmati (`apps/events/services.py`):**
  - [x] `register_for_event(user, event)` logikasi.
  - [x] **BR-1:** Bir foydalanuvchi bir tadbirga faqat 1 marta yoziladi (mavjud bo'lsa xato yoki qayta faollashtirish).
  - [x] **BR-2:** `capacity` tekshiruvi (agar to'lgan bo'lsa `code: event_full`).
  - [x] **BR-3:** Boshlangan yoki o'tib ketgan tadbirga yozilish taqiqlanadi (`code: event_started`).
  - [x] **BR-5:** Yopilgan tadbirga yozilish taqiqlanadi (`code: event_closed`).
  - [x] **Race condition himoyasi:** `with transaction.atomic(): Event.objects.select_for_update()`.
- [x] **Tadbirdan chiqish xizmati (`apps/events/services.py`):
  - [x] `unregister_from_event(user, event)` logikasi.
  - [x] **BR-6:** Boshlangan tadbirdan chiqish taqiqlanadi (`code: event_started`).
  - [x] `status = cancelled`, `cancelled_at = now()` belgilanadi va tadbirdagi joy boshqalarga ochiladi.
- [x] **Ro'yxatdan o'tish API Endpointlari:**
  - [x] `POST /api/v1/events/{id}/register/` — tadbirga yozilish (login qilgan user).
  - [x] `POST /api/v1/events/{id}/unregister/` — tadbirdan chiqish (login qilgan user).
  - [x] `GET /api/v1/me/registrations/` — **BR-10**: foydalanuvchi faqat o'zi yozilgan tadbirlarni ko'radi (`?status=active/cancelled`).
  - [x] `GET /api/v1/events/{id}/participants/` — faqat admin uchun: faol qatnashuvchilar ro'yxati (ism, email, telefon).

---

## 6-BOSQICH: Telegram Bot Integratsiyasi va Xabarnomalar
*Telegram hisobini bog'lash, bildirishnomalar va xavfsiz aloqa.*

- [x] **Telegram bog'lash API ([apps/notifications/views.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/notifications/views.py)):**
  - [x] `POST /api/v1/telegram/link/` — tasodifiy xavfsiz token (`secrets.token_urlsafe(16)`) yaratish va havola berish (`t.me/EventlyBot?start=TOKEN`).
  - [x] `POST /api/v1/telegram/confirm/` — Bot tomonidan `chat_id` ni tasdiqlash (`X-Bot-Secret` maxfiy kalit tekshiruvi bilan).
  - [x] Serializerlar ([apps/notifications/serializers.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/notifications/serializers.py)): `TelegramLinkResponseSerializer`, `TelegramConfirmRequestSerializer`, `TelegramConfirmResponseSerializer`.
  - [x] Marshrutlar ([apps/notifications/urls.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/notifications/urls.py)) API v1 ga ulandi.
- [x] **Xabarnomalar servisi ([apps/notifications/services.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/notifications/services.py)):**
  - [x] Telegram Bot API (`sendMessage`) integratsiyasi (`send_telegram_message`).
  - [x] `transaction.on_commit(...)` orqali faqat DB tranzaksiyasi to'liq yakunlangach xabar yuborish.
  - [x] `try/except` xavfsiz himoyasi: Telegram xizmati ishlamay qolsa ham ro'yxatdan o'tish tranzaksiyasi buzilmaydi.
- [x] **Bildirishnomalar (T1):**
  - [x] Ro'yxatdan o'tganda foydalanuvchiga tasdiq xabari yuborish (`notify_user_registration`: Tadbir nomi, sana, joy).
  - [x] Yangi qatnashuvchi yozilganda barcha adminlarga bildirishnoma yuborish (`notify_admins_new_registration`: Ism, telefon, band joylar).

---

## 7-BOSQICH: Avtomatik Eslatmalar Mexanizmi (Reminders)
*Tadbirdan 24 soat oldin bot orqali avtomatik eslatma jo'natish.*

- [x] **Management Command ([apps/notifications/management/commands/send_event_reminders.py](file:///C:/Users/User/Desktop/NajotTalim/PROJECT/evently/apps/notifications/management/commands/send_event_reminders.py)):**
  - [x] `python manage.py send_event_reminders [--hours 24]` komandasi yaratildi.
- [x] **Eslatma Logikasi (T2):**
  - [x] `status='active'`, `reminder_sent=False`, `event.status='open'` bo'lgan yozuvlarni tanlash.
  - [x] Boshlanishiga `REMINDER_HOURS_BEFORE` (24 soat) qolgan tadbirlarni topish.
  - [x] Bog'langan foydalanuvchilarga eslatma yuborish va `reminder_sent = True` belgilash (ikki marta bormasligi kafolatlangan).
- [x] **Davriy ishga tushirish (Cron):**
  - [x] Har 10 daqiqada ishga tushirish qo'llanmasi:
    ```bash
    */10 * * * * cd /path/to/evently && /path/to/venv/bin/python manage.py send_event_reminders >> /var/log/evently_reminders.log 2>&1
    ```

---

## 8-BOSQICH: Alohida aiogram 3.x Telegram Bot Dasturi
*Foydalanuvchi bilan Telegram orqali muloqot qiluvchi asinxron bot.*

- [ ] **Bot tuzilmasi (`bot/`):**
  - [ ] `bot/config.py` — Bot tokeni, backend URL va maxfiy kalitlar.
  - [ ] `bot/api_client.py` — Backend API bilan xavfsiz HTTP muloqot (httpx/aiohttp).
  - [ ] `bot/handlers.py` — `/start`, `/help`, `/start <token>` (deep linking tekshiruv va tasdiq).
  - [ ] `bot/main.py` — aiogram botni alohida jarayonda ishga tushirish (`python -m bot.main`).

---

## 9-BOSQICH: Namunaviy Ma'lumotlar Yaratish (Seed Data)
*Loyihani tekshirish va ko'rgazma uchun test ma'lumotlarini kiritish.*

- [ ] **Management Command:**
  - [ ] `python manage.py seed_data` komandasi yaratiladi.
- [ ] **Yaratiladigan ma'lumotlar:**
  - [ ] 2 ta Admin hisobi (`admin1@example.com`, `admin2@example.com`).
  - [ ] 10 ta oddiy foydalanuvchi hisobi.
  - [ ] 15 ta turli holatdagi tadbirlar (kelajakdagi, o'tgan, ochiq, yopiq, cheklangan sig'imli).

---

## 10-BOSQICH: Sifat Nazorati va To'liq Integratsion Testlar
*Loyiha himoyasi va xatolardan himoyalanganlik kafolati.*

- [x] **Mavjud va yangi qo'shilgan testlar (50 ta PASS):**
  - [x] Auth testlari (12 ta): ro'yxatdan o'tish, login, profil, rol xavfsizligi.
  - [x] Core/Settings testlari (5 ta): health check, custom pagination, exception handler, CORS, logs.
  - [x] Events CRUD testlari (12 ta): model propertilari, admin ruxsatlari, BR-7, BR-8, BR-9 validatsiyalari, filter va search.
  - [x] `test_registration_success` (ochiq tadbirga muvaffaqiyatli yozilish).
  - [x] `test_registration_br1_duplicate` (ikki marta yozilish taqiqlanishi).
  - [x] `test_registration_br2_capacity_full` (sig'im to'lganda yozilib bo'lmasligi).
  - [x] `test_registration_br3_event_started` (boshlangan tadbirga yozilmasligi).
  - [x] `test_registration_br5_event_closed` (yopilgan tadbirga yozilmasligi).
  - [x] `test_unregister_br6_after_start` (boshlangan tadbirdan chiqib bo'lmasligi).
  - [x] `test_unregister_and_re_register` (chiqib qayta yozilganda joy ochilishi).
  - [x] `test_my_registrations_br10` (faqat o'z tadbirlarini ko'rish).
  - [x] `test_participants_list_admin_only` (oddiy userga 403, adminga 200).
  - [x] `test_telegram_link_success` va `test_telegram_link_unauthenticated`.
  - [x] `test_telegram_confirm_success_and_wrong_secret` (X-Bot-Secret tekshiruvi).
  - [x] `test_telegram_send_failure_does_not_break_registration` (Mock bilan).
  - [x] `test_registration_triggers_user_and_admin_notifications` (Tranzaksiya commit bo'lganda bildirishnoma).
  - [x] `test_reminder_command_only_sent_once` (eslatma 1 marta borishi).

---

## 11-BOSQICH: Production Deployment va Yakuniy Topshirish
*Loyihani serverga o'rnatish va topshirishga tayyorlash.*

- [ ] **Production Sozlamalari:**
  - [ ] `DEBUG=False`, `ALLOWED_HOSTS` sozlash.
  - [ ] `collectstatic` orqali statik fayllarni yig'ish (Swagger va Admin UI to'liq ko'rinishi).
  - [ ] Gunicorn WSGI server orqali ishga tushirish.
- [ ] **Platformaga joylashtirish (Render / Railway / VPS):**
  - [ ] PostgreSQL ma'lumotlar bazasini ulash.
  - [ ] Django API va aiogram Botni alohida xizmat sifatida ishga tushirish.
  - [ ] Cron job yoki davriy eslatmalar xizmatini yoqish.
- [ ] **Yakuniy Hujjat:**
  - [ ] Asosiy `README.md` ni shaxsiy loyiha tavsifi bilan yangilash.
  - [ ] Swagger va jonli API havolalarini taqdim etish.
