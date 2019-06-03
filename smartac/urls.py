from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import RedirectView

from allauth import urls as allauth_urls
from invitations import urls as invitations_urls
from rest_framework.routers import DefaultRouter

from .devices import views as device_views


admin.site.site_header = _('SmartAC Admin')
admin.site.site_title = _('SmartAC Admin')
admin.site.index_title = _('Welcome to the SmartAC Admin!')

router = DefaultRouter()
router.register('devices', device_views.DeviceCreateViewSet)
router.register('sensor_logs', device_views.DeviceSensorLogCreateViewSet)
router.register('health_status', device_views.DeviceHealthStatusCreateViewSet)

urlpatterns = [
    path(
        'admin/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='admin_password_reset',
    ),
    path(
        'admin/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path('admin/', admin.site.urls),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),

    path('invitations/', include(invitations_urls, namespace='invitations')),
    path('accounts/', include(allauth_urls)),

    path('api/v1/', include(router.urls)),

    # Default to admin index
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('admin:index'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
