
from django.urls import path
from .views import viewregister
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView)

app_name = "app_user"

urlpatterns = [
    path('password-reset/', PasswordResetView.as_view(template_name="app_user/password_reset.html"),
         name="password_reset"),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="app_user/password_reset_done.html"),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="app_user/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name="app_user/password_reset_complete.html"),
         name="password_reset_complete"),
]

