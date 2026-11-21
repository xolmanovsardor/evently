from django.db import transaction
from django.utils import timezone
from config.exceptions import BusinessLogicError
from apps.events.models import Event, EventStatus, Registration, RegistrationStatus
from apps.notifications.services import handle_registration_notifications


def register_for_event(user, event: Event) -> Registration:
    """
    Tadbirga yozilish xizmati (BR-1, BR-2, BR-3, BR-5 va Race Condition himoyasi).
    """
    # BR-5: Tadbir yopilgan bo'lsa
    if event.status == EventStatus.CLOSED:
        raise BusinessLogicError(
            detail="Tadbir yopilgan.",
            code="event_closed"
        )

    # BR-3: Tadbir boshlangan bo'lsa
    if event.start_at <= timezone.now():
        raise BusinessLogicError(
            detail="Tadbir allaqachon boshlangan.",
            code="event_started"
        )

    # BR-1: Foydalanuvchi allaqachon yozilgan bo'lsa
    existing_reg = Registration.objects.filter(user=user, event=event).first()
    if existing_reg and existing_reg.status == RegistrationStatus.ACTIVE:
        raise BusinessLogicError(
            detail="Siz bu tadbirga allaqachon yozilgansiz.",
            code="already_registered"
        )

    # Race condition himoyasi: select_for_update orqali qulflash
    with transaction.atomic():
        locked_event = Event.objects.select_for_update().get(id=event.id)

        # BR-5 & BR-3 qayta tekshiruv (tranzaksiya ichida)
        if locked_event.status == EventStatus.CLOSED:
            raise BusinessLogicError(detail="Tadbir yopilgan.", code="event_closed")
        if locked_event.start_at <= timezone.now():
            raise BusinessLogicError(detail="Tadbir allaqachon boshlangan.", code="event_started")

        # BR-2: Sig'im tekshiruvi
        active_count = locked_event.registrations.filter(status=RegistrationStatus.ACTIVE).count()
        if locked_event.capacity is not None and active_count >= locked_event.capacity:
            raise BusinessLogicError(
                detail="Bo‘sh joy qolmagan.",
                code="event_full"
            )

        if existing_reg:
            # Chiqib ketgan foydalanuvchi qayta yozilmoqda
            existing_reg.status = RegistrationStatus.ACTIVE
            existing_reg.cancelled_at = None
            existing_reg.reminder_sent = False
            existing_reg.save(update_fields=['status', 'cancelled_at', 'reminder_sent'])
            reg = existing_reg
        else:
            reg = Registration.objects.create(
                user=user,
                event=locked_event,
                status=RegistrationStatus.ACTIVE
            )

        transaction.on_commit(lambda: handle_registration_notifications(user, locked_event))

    return reg


def unregister_from_event(user, event: Event) -> Registration:
    """
    Tadbirdan chiqish xizmati (BR-6).
    """
    # BR-6: Tadbir boshlangan bo'lsa chiqib bo'lmaydi
    if event.start_at <= timezone.now():
        raise BusinessLogicError(
            detail="Tadbir allaqachon boshlangan.",
            code="event_started"
        )

    reg = Registration.objects.filter(
        user=user,
        event=event,
        status=RegistrationStatus.ACTIVE
    ).first()

    if not reg:
        raise BusinessLogicError(
            detail="Siz bu tadbirga yozilmagansiz.",
            code="not_registered"
        )

    reg.status = RegistrationStatus.CANCELLED
    reg.cancelled_at = timezone.now()
    reg.save(update_fields=['status', 'cancelled_at'])
    return reg


@transaction.atomic
def create_event(*, title, description, event_type, location, start_at, end_at, capacity=None, created_by=None) -> Event:
    return Event.objects.create(
        title=title,
        description=description,
        event_type=event_type,
        location=location,
        start_at=start_at,
        end_at=end_at,
        capacity=capacity,
        created_by=created_by,
        status=EventStatus.OPEN
    )


@transaction.atomic
def update_event(*, event_id: int, **fields) -> Event:
    event = Event.objects.select_for_update().get(id=event_id)

    if 'capacity' in fields:
        new_capacity = fields['capacity']
        if new_capacity is not None and new_capacity < event.registered_count:
            raise BusinessLogicError(
                detail="Joylar soni hozirgi qatnashuvchilar sonidan kam bo‘lishi mumkin emas.",
                code="capacity_too_low"
            )

    for field, value in fields.items():
        setattr(event, field, value)

    event.save()
    return event


@transaction.atomic
def close_event(*, event_id: int) -> Event:
    event = Event.objects.select_for_update().get(id=event_id)
    event.status = EventStatus.CLOSED
    event.save(update_fields=['status', 'updated_at'])
    return event
