from rest_framework import serializers


class TelegramLinkResponseSerializer(serializers.Serializer):
    link = serializers.CharField(help_text="Telegram bot start havolasi")
    token = serializers.CharField(help_text="Generatsiya qilingan vaqtinchalik token")


class TelegramConfirmRequestSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, help_text="Vaqtinchalik tasdiqlash tokeni")
    chat_id = serializers.IntegerField(required=True, help_text="Foydalanuvchining Telegram chat ID raqami")


class TelegramConfirmResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
