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
	'Security' : 'Sc',
	'Advertise' : 'Ad',
	'General' : 'Gn',
	'Offer' : 'Of'
}

class Notification(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4)
	unix_time = models.CharField(max_length=13, db_index=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	label = models.CharField(max_length=2, choices=_NOTIFICATION_LABEL, default='Gn')
	title = models.TextField()
	message = models.TextField()
	action = models.TextField(default='#')
	seen = models.BooleanField(default=False)


class TrendingSpaceStatus(models.Model):
	status = models.OneToOneField(Status, on_delete=models.CASCADE, primary_key=True)



class PinnedProduct(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	unix_time = models.CharField(max_length=13)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)



class Favorite(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	unix_time = models.CharField(max_length=13, db_index=True)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
