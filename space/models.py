from account.models import Account

from django.db import models



_CATEGORY = (
	('Q', 'Q'),
	('T', 'T')
)

class Space(models.Model):
	"""
	Doc here
	"""
	owner = models.OneToOneField(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, unique=True)
	description = models.TextField()
	category = models.CharField(max_length=10, choices=_CATEGORY)
	logo = models.TextField()
	cover = models.TextField()
	# unknown field types
	# -->
	rating = models.PositiveSmallIntegerField(default=0)
	location_zone = models.BooleanField(default=False)


class Product(models.Model):
	"""
	Doc here
	"""
	price = models.FloatField()
	description = models.TextField()
	time_date = models.DateTimeField(auto_now=True)
	space = models.OneToOneField(Account, on_delete=models.CASCADE)


class PostMedia(models.Model):
	"""
	Doc here
	"""
	location = models.CharField(max_length=100)
	in_stack = models.BooleanField(default=True)
	is_image = models.BooleanField(default=True)
	product = models.OneToOneField(Product, on_delete=models.CASCADE)



class Sell(models.Model):
	"""
	Doc here
	"""
	by = models.ForeignKey(Space, on_delete=models.CASCADE)
	to = models.ForeignKey(Account, null=True, blank=True,on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
