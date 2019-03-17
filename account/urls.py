from django.urls import path
from account.views import auth, manage

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetForm

urlpatterns = [
	
	path('', manage.profile, name='account_profile'),
	path('activity/', manage.activity_manager, name='activity_manager'),

	path('signup/', auth.signup, name='account_signup'),
	path('signin/', auth.signin, name='account_signin'),
	path('signout/', auth.signout, name='account_signout'),
    path('change-password/', auth.change_password, name='change_password'),

	path('update/', manage.update, name='account_update'),
	path('delete/', manage.delete, name='account_delete'),
	path('deactivate/', manage.decactive, name='account_deactivate'),


	path('password-reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]