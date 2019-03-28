from django.urls import path,include

from home.views import manage, filtering

urlpatterns = [
	path('', manage.manager , name='view-manager'),
	path('notification/', manage.notification, name='notification'),
	path('notification/<uid>/', manage.notification_status_changle, name='notification-status-change'),
	
	path('trending/', filtering.trending, name='trending-spaces'),
]