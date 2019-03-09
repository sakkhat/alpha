from django.urls import path
from .views import auth, manage,password

urlpatterns = [
	
	path('', manage.info, name='account_info'),

	path('signup/', auth.signup, name='account_signup'),
	path('signin/', auth.signin, name='account_signin'),
	path('signout/', auth.signout, name='account_signout'),

	path('update/', manage.update, name='account_update'),
	path('delete/', manage.delete, name='account_delete'),
	path('deactivate/', manage.decactive, name='account_deactivate'),

	path('password/', password.manager, name='account_password'),
]