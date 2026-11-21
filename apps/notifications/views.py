import secrets
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.notifications.serializers import (
    TelegramLinkResponseSerializer,
    TelegramConfirmRequestSerializer,
    TelegramConfirmResponseSerializer,
)

User = get_user_model()


class TelegramLinkView(APIView):
    """
    Foydalanuvchining hisobini Telegram botga bog'lash uchun bir martalik havola va token olish.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Telegram hisobini bog'lash havolasini olish",
        description="Foydalanuvchi hisobiga biriktirilgan unikal token va bot havolasini qaytaradi.",
        responses={200: TelegramLinkResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        token = secrets.token_urlsafe(16)
        user = request.user
        user.telegram_link_token = token
        user.save(update_fields=['telegram_link_token'])

        bot_username = getattr(settings, 'TELEGRAM_BOT_USERNAME', 'EventlyBot')
        link = f"https://t.me/{bot_username}?start={token}"

        serializer = TelegramLinkResponseSerializer(data={"link": link, "token": token})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TelegramConfirmView(APIView):
    """
    Telegram bot tomonidan foydalanuvchining chat_id sini tasdiqlash endpointi.
    X-Bot-Secret sarlavhasi orqali himoyalangan.
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Telegram chat_id tasdiqlash (Faqat Bot uchun)",
        description="Bot maxfiy kalit (X-Bot-Secret) orqali tokenni tekshiradi va chat_id ni foydalanuvchiga bog'laydi.",
        request=TelegramConfirmRequestSerializer,
        responses={
            200: TelegramConfirmResponseSerializer,
            400: OpenApiResponse(description="Yaroqsiz token yoki ma'lumotlar"),
            403: OpenApiResponse(description="Noto'g'ri maxfiy kalit"),
        }
    )
    def post(self, request, *args, **kwargs):
        # Maxfiy kalitni tekshirish
        bot_secret = request.headers.get('X-Bot-Secret')
        expected_secret = getattr(settings, 'BOT_API_SECRET', '')

        if not expected_secret or bot_secret != expected_secret:
            return Response(
                {"detail": "Noto'g'ri maxfiy kalit."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TelegramConfirmRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        chat_id = serializer.validated_data['chat_id']

        # Token bo'yicha foydalanuvchini topish
        user = User.objects.filter(telegram_link_token=token).first()
        if not user:
            return Response(
                {"detail": "Yaroqsiz yoki eskirgan token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Agar ushbu chat_id boshqa akkauntda bo'lsa, tozalaymiz (unikal bo'lishi uchun)
        User.objects.filter(telegram_chat_id=chat_id).exclude(id=user.id).update(telegram_chat_id=None)

        user.telegram_chat_id = chat_id
        user.telegram_link_token = None
        user.save(update_fields=['telegram_chat_id', 'telegram_link_token'])

        response_data = {
            "detail": "Telegram hisobi muvaffaqiyatli bog'landi.",
            "email": user.email,
            "full_name": user.full_name or user.email,
        }
        return Response(response_data, status=status.HTTP_200_OK)
