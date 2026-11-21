from django.urls import path
from apps.notifications.views import TelegramLinkView, TelegramConfirmView

app_name = 'notifications'

urlpatterns = [
    path('telegram/link/', TelegramLinkView.as_view(), name='telegram-link'),
    path('telegram/confirm/', TelegramConfirmView.as_view(), name='telegram-confirm'),
]
