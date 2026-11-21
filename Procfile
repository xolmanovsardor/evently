web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3
bot: python -m bot.main
worker: python manage.py send_event_reminders
