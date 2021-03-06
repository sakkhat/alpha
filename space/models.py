from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from account.models import Account

from uuid import uuid4



_PRODDUCT_CATEGORY = (
	('Ots', 'Others'),
	('GnA', 'Gadget-Accessories'),
	('MFs', 'Men-Fashion'),
	('WFs', 'Women-Fashion'),
)

_PRODDUCT_CATEGORY_DIC = {
	'Ots': 'Others',
	'GnA': 'Gadget-Accessories',
	'MFs': 'Men-Fashion',
	'WFs': 'Women-Fashion',
}

_PRODDUCT_CATEGORY_KEY_DIC = {
	'others' : 'Ots',
	'gadget-accessories' : 'GnA',
	'men-fashion' : 'MFs',
	'women-fashion' : 'WFs',
}


_PRODUCT_REACT = (
	('G', 'Good'),
	('B', 'Bad'),
	('F', 'Fake')
)

class Category(models.Model):
	"""
	Doc here
	"""
	name = models.CharField(max_length=3, choices=_PRODDUCT_CATEGORY, default='Ots',unique=True)
	logo_url = models.CharField(max_length=150)
	cover_url = models.CharField(max_length=150)
	total_products = models.PositiveIntegerField(default=0)

	def __str__(self):
		return _PRODDUCT_CATEGORY_DIC[self.name]


class Space(models.Model):
	"""
	Doc here
	"""
	owner = models.OneToOneField(Account, on_delete=models.CASCADE)
	logo = models.CharField(max_length=150)
	name = models.CharField(max_length=20, unique=True)
	display_name = models.CharField(max_length=50)
	description = models.TextField(max_length=1500)
	join = models.DateTimeField(auto_now_add=True)
	code = models.DecimalField(max_digits=24, decimal_places=0, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		models.Index(fields=['code', 'owner'])



class Banner(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	location = models.CharField(default='/static/res/space_banner.JPG', max_length=150)



class Product(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	title = models.CharField(max_length=30)
	price = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(999999.99)])
	description = models.TextField(max_length=1500)
	logo_url = models.CharField(max_length=150)
	time_date = models.DateTimeField(auto_now=True)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
	in_stock = models.BooleanField(default=True)
	react_good = models.PositiveIntegerField(default=0)
	react_bad = models.PositiveIntegerField(default=0)
	react_fake = models.PositiveIntegerField(default=0)
	phone_request = models.BooleanField(default=True)
	email_request = models.BooleanField(default=True)



class ProductReact(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	time_date = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	react = models.CharField(max_length=1, choices=_PRODUCT_REACT)

	class Meta:
		unique_together = ('user', 'product')



class ProductMedia(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	location = models.CharField(max_length=150)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.location


class Status(models.Model):
	"""
	Doc here
	"""
	space = models.OneToOneField(Space, on_delete=models.CASCADE,primary_key=True)
	total_good_react = models.PositiveIntegerField(default=0)
	total_bad_react = models.PositiveIntegerField(default=0)
	total_fake_react = models.PositiveIntegerField(default=0)
	total_favorite = models.PositiveIntegerField(default=0)
	total_pinned = models.PositiveIntegerField(default=0)
	total_post = models.PositiveIntegerField(default=0)
	rating = models.PositiveIntegerField(default=0)
