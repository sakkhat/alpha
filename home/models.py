from django.db import models

from account.models import Account
from space.models import Space,Product


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
	uid = models.CharField(max_length=13, unique=True, primary_key=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	label = models.CharField(max_length=2, choices=_NOTIFICATION_LABEL, default='Gn')
	title = models.TextField()
	message = models.TextField()
	action = models.TextField(default='#')
	seen = models.BooleanField(default=False)


class TrendingSpace(models.Model):
	space = models.OneToOneField(Space, on_delete=models.CASCADE, primary_key=True)


class TrendingProduct(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)


class PinnedProduct(models.Model):
	"""
	Doc here
	"""
	uid = models.CharField(max_length=13, unique=True, primary_key=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)



class Favorite(models.Model):
	"""
	Doc here
	"""
	uid = models.CharField(max_length=13, unique=True, primary_key=True)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
