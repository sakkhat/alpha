from django.db import models

from account.models import Account
from space.models import Status,Product,Space

from uuid import uuid4


_NOTIFICATION_LABEL = (
	('Sc', 'Security'),
	('Ad', 'Advertise'),
	('Gn', 'General'),
	('Of', 'Offer'),
)

_NOTIFICATION_LABEL_DIC = {
	'security' : 'Sc',
	'advertise' : 'Ad',
	'general' : 'Gn',
	'offer' : 'Of'
}

class Notification(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4)
	time_date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	label = models.CharField(max_length=2, choices=_NOTIFICATION_LABEL, default='Gn')
	title = models.CharField(max_length=50)
	message = models.TextField()
	action = models.CharField(max_length=120, default='#')
	seen = models.BooleanField(default=False)




class PinnedProduct(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	time_date = models.DateTimeField(auto_now_add=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)



class Favorite(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	time_date = models.DateTimeField(auto_now_add=True)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
