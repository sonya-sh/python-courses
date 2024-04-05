from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView
)

from .views import RegistrationView, UserProfile, UserProfileEdit

urlpatterns = [

    path('registration/', RegistrationView.as_view(), name='registration'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),

    path('accounts/password_change/', PasswordChangeView.as_view(
        template_name='users/password_change.html'
        ), name='password_change'),

    path('accounts/password_change/done', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
        ), name='password_change_done'),

    path('accounts/profile/', UserProfile.as_view(), name='profile'),
    path('accounts/profile/edit/', UserProfileEdit.as_view(), name='profile_edit'),

    path('accounts/password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),

    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('password_reset_complete')
    ), name='password_reset_confirm'),

    path('accounts/reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]



"""
accounts/ login/ [name='login']
accounts/ logout/ [name='logout']

accounts/ password_change/ [name='password_change']
accounts/ password_change/done/ [name='password_change_done']

accounts/ password_reset/ [name='password_reset']
accounts/ password_reset/done/ [name='password_reset_done']
accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/ reset/done/ [name='password_reset_complete']

"""