from django.db import models

from account.models import Account
from space.models import Space,Product

class TrendingSpace(models.Model):
	space = models.OneToOneField(Space, on_delete=models.CASCADE, primary_key=True)


class TrendingProduct(models.Model):
	product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)


class PinnedProduct(models.Model):
	"""
	Doc here
	"""
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('product', 'user')



class Favorite(models.Model):
	"""
	Doc here
	"""
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('space','user')