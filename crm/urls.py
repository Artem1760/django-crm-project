from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path, include, reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls', namespace='landing')),
    path('tickets/', include('tickets.urls', namespace='tickets')),
    path('associates/', include('associates.urls', namespace='associates')),

    # Reset password
    path('reset-password/', PasswordResetView.as_view(
        template_name='password_reset/password_reset_form.html',
        success_url=reverse_lazy('password-reset-done'),
        email_template_name='password_reset/password_reset_email.html'),
         name='password-reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(
        template_name='password_reset/password_reset_done.html'),
         name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='password_reset/password_reset_confirm.html',
             success_url=reverse_lazy('password-reset-complete')),
         name='password-reset-confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_complete.html'),
         name='password-reset-complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
