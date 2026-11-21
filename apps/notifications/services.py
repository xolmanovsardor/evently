import logging
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.events.models import Event

logger = logging.getLogger('telegram')
User = get_user_model()


def send_telegram_message(chat_id: int, text: str) -> bool:
    """
    Telegram Bot API orqali xabar yuborish servisi.
    Xatolik yuz berganda istisno chiqarmaydi, logga yozadi va False qaytaradi.
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    if not token or not chat_id:
        logger.warning(f"Telegram token yoki chat_id yo'q. chat_id={chat_id}")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"Telegram xabari muvaffaqiyatli yuborildi: chat_id={chat_id}")
            return True
        else:
            logger.error(
                f"Telegram API xatolik qaytardi: status={response.status_code}, body={response.text}"
            )
            return False
    except Exception as exc:
        logger.error(f"Telegram xabar yuborishda ulanish xatosi: {str(exc)}", exc_info=True)
        return False


def notify_user_registration(user, event: Event) -> bool:
    """
    Foydalanuvchi tadbirga ro'yxatdan o'tganda unga Telegram orqali tasdiq xabari yuborish (T1).
    """
    if not user.telegram_chat_id:
        return False

    formatted_time = event.start_at.strftime("%d.%m.%Y %H:%M")
    message = (
        f"🎉 <b>Tadbirga muvaffaqiyatli yozildingiz!</b>\n\n"
        f"📌 <b>Tadbir:</b> {event.title}\n"
        f"📅 <b>Boshlanish vaqti:</b> {formatted_time}\n"
        f"📍 <b>Manzil:</b> {event.location}\n\n"
        f"<i>Tadbirdan 24 soat oldin sizga eslatma yuboramiz.</i>"
    )
    return send_telegram_message(user.telegram_chat_id, message)


def notify_admins_new_registration(event: Event, user) -> int:
    """
    Yangi qatnashuvchi yozilganda barcha bog'langan adminlarga bildirishnoma yuborish (T1).
    """
    admins = User.objects.filter(role='admin', telegram_chat_id__isnull=False)
    if not admins.exists():
        return 0

    count = event.registrations.filter(status='active').count()
    capacity_str = str(event.capacity) if event.capacity is not None else "Cheksiz"
    user_name = user.full_name or user.email
    phone = user.phone_number or "Kiritilmagan"

    message = (
        f"📢 <b>Yangi ro'yxatdan o'tish!</b>\n\n"
        f"📌 <b>Tadbir:</b> {event.title}\n"
        f"👤 <b>Qatnashuvchi:</b> {user_name}\n"
        f"📞 <b>Telefon:</b> {phone}\n"
        f"👥 <b>Band joylar:</b> {count}/{capacity_str}"
    )

    sent_count = 0
    for admin in admins:
        if send_telegram_message(admin.telegram_chat_id, message):
            sent_count += 1
    return sent_count


def handle_registration_notifications(user, event: Event) -> None:
    """
    Tranzaksiya muvaffaqiyatli yakunlangach chaqiriladigan xavfsiz wrapper.
    Xatolik bo'lsa ham tranzaksiya yoki API ga ta'sir qilmaydi.
    """
    try:
        notify_user_registration(user, event)
    except Exception as e:
        logger.error(f"Foydalanuvchiga bildirishnoma yuborishda xatolik: {e}")

    try:
        notify_admins_new_registration(event, user)
    except Exception as e:
        logger.error(f"Adminlarga bildirishnoma yuborishda xatolik: {e}")
