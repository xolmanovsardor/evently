from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from config.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health Check
    path('api/v1/health/', HealthCheckView.as_view(), name='health-check'),

    # API Documentation (Swagger & Redoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1 routes
    path('api/v1/auth/', include('apps.users.urls', namespace='auth')),
    path('api/v1/', include('apps.notifications.urls', namespace='notifications')),
    path('api/v1/', include('apps.events.urls', namespace='events')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

