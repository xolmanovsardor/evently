import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from apps.events.models import Registration, RegistrationStatus, EventStatus
from apps.notifications.services import send_telegram_message

logger = logging.getLogger('telegram')


class Command(BaseCommand):
    help = "Tadbirdan 24 soat oldin foydalanuvchilarga avtomatik Telegram eslatma yuborish (T2)."

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=getattr(settings, 'REMINDER_HOURS_BEFORE', 24),
            help="Qancha vaqt oldin eslatma jo'natish (soatlarda, default: 24)"
        )

    def handle(self, *args, **options):
        hours = options.get('hours')
        now = timezone.now()
        target_time = now + timedelta(hours=hours)

        self.stdout.write(
            f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Eslatmalar yuborish boshlandi (Oraliq: keyingi {hours} soat)..."
        )

        # Eslatma yuborilishi kerak bo'lgan faol ro'yxatdan o'tganlar:
        # 1. registration.status == 'active'
        # 2. registration.reminder_sent == False
        # 3. event.status == 'open'
        # 4. now < event.start_at <= now + hours
        # 5. user.telegram_chat_id is not null
        registrations = (
            Registration.objects.select_related('user', 'event')
            .filter(
                status=RegistrationStatus.ACTIVE,
                reminder_sent=False,
                event__status=EventStatus.OPEN,
                event__start_at__gt=now,
                event__start_at__lte=target_time,
            )
        )

        count = 0
        skipped = 0

        for reg in registrations:
            user = reg.user
            event = reg.event

            if not user.telegram_chat_id:
                # Telegram ulanmagan bo'lsa ham kelgusida qayta urinmaslik uchun belgilab qo'yish mumkin
                skipped += 1
                reg.reminder_sent = True
                reg.save(update_fields=['reminder_sent'])
                continue

            formatted_time = event.start_at.strftime("%d.%m.%Y %H:%M")
            message = (
                f"⏰ <b>Eslatma! Tadbiringiz yaqinlashmoqda!</b>\n\n"
                f"📌 <b>Tadbir:</b> {event.title}\n"
                f"📅 <b>Boshlanish vaqti:</b> {formatted_time}\n"
                f"📍 <b>Manzil:</b> {event.location}\n\n"
                f"<i>Sizni tadbirimizda kutib qolamiz!</i>"
            )

            success = send_telegram_message(user.telegram_chat_id, message)
            if success:
                count += 1
                reg.reminder_sent = True
                reg.save(update_fields=['reminder_sent'])
                self.stdout.write(self.style.SUCCESS(f"  -> {user.email} ga eslatma yuborildi ({event.title})"))
            else:
                self.stdout.write(self.style.WARNING(f"  -> {user.email} ga eslatma yuborishda xatolik yuz berdi"))

        self.stdout.write(
            self.style.SUCCESS(f"Jami yuborildi: {count} ta, Telegram bog'lanmagan: {skipped} ta.")
        )
