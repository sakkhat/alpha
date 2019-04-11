from django.db import models

from account.models import Account

from generic.variables import DISTRICTS

from uuid import uuid4



_PRODDUCT_CATEGORY = (
	('Ots', 'Others'),
	('Gdt', 'Gadget'),
	('MFs', 'Man Fashion'),
	('WFs', 'Woman Fashion'),
	('CAc', 'Computer Accessory'),
	('Elc', 'Electronics')
)

_PRODDUCT_CATEGORY_DIC = {
	'Ots': 'Others',
	'Gdt': 'Gadget',
	'MFs': 'Man Fashion',
	'WFs': 'Woman Fashion',
	'CAc': 'Computer Accessory',
	'Elc': 'Electronics',
}

_PRODDUCT_CATEGORY_KEY_DIC = {
	'Others' : 'Ots',
	'Gadget' : 'Gdt',
	'Man-Fashion' : 'MFs',
	'Woman-Fashion' : 'WFs',
	'Computer-Accessory' : 'CAc',
	'Electronics' : 'Elc',
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
	name = models.CharField(max_length=3, choices=_PRODDUCT_CATEGORY, default='Ots',primary_key=True)
	logo_url = models.TextField()
	cover_url = models.TextField()
	total_products = models.PositiveIntegerField(default=0)


	def __str__(self):
		return _PRODDUCT_CATEGORY_DIC[self.name]




class Space(models.Model):
	"""
	Doc here
	"""
	owner = models.OneToOneField(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, unique=True)
	description = models.TextField()
	join = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.name + ' : '+self.uid



class Banner(models.Model):
	uid = models.UUIDField(primary_key=True, default=uuid4)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	location = models.TextField(default='https://i.postimg.cc/GmzSz9Nq/banner.png')



class Product(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	title = models.CharField(max_length=30)
	price = models.FloatField()
	description = models.TextField()
	logo_url = models.TextField()
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
	unix_time = models.CharField(max_length=13, db_index=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	react = models.CharField(max_length=1, choices=_PRODUCT_REACT)



class ProductMedia(models.Model):
	"""
	Doc here
	"""
	uid = models.UUIDField(primary_key=True, default=uuid4)
	location = models.TextField(unique=True)
	is_image = models.BooleanField(default=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.location


class Status(models.Model):
	"""
	Doc here
	"""
	space = models.OneToOneField(Space, primary_key=True, on_delete=models.CASCADE)
	total_good_react = models.PositiveIntegerField(default=0)
	total_bad_react = models.PositiveIntegerField(default=0)
	total_fake_react = models.PositiveIntegerField(default=0)
	total_favorite = models.PositiveIntegerField(default=0)
	total_pinned = models.PositiveIntegerField(default=0)
	total_post = models.PositiveIntegerField(default=0)
	rating = models.PositiveIntegerField(default=0)

