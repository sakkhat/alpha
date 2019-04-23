from django.urls import path
from account.views import auth, manage

from django.contrib.auth import views as resetviews

urlpatterns = [
	
	path('', manage.profile, name='account_profile'),
	path('activity/', manage.activity_manager, name='activity_manager'),

	path('signup/', auth.signup, name='account-signup'),
	path('verify/<token>/', auth.verify, name='account-verify'),
	path('signin/', auth.signin, name='account-signin'),
	path('signout/', auth.signout, name='account-signout'),
    path('change-password/', auth.change_password, name='change-password'),

	path('update/', manage.update, name='account-update'),
	path('delete/', manage.delete, name='account-delete'),
	path('deactivate/', manage.decactive, name='account-deactivate'),


	path('password-reset/', resetviews.PasswordResetView.as_view(
        template_name='account/password/reset.html'),name='password_reset'),

    path('password-reset/done/', resetviews.PasswordResetDoneView.as_view(
        template_name='account/password/reset-done.html'),name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', resetviews.PasswordResetConfirmView.as_view(
        template_name='account/password/reset-confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/', resetviews.PasswordResetCompleteView.as_view(
        template_name='account/password/reset-complete.html'), name='password_reset_complete'),
]