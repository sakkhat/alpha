from django.db import models

from account.models import Account

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

	def __str__(self):
		return _PRODDUCT_CATEGORY_DIC[self.name]


class Space(models.Model):
	"""
	Doc here
	"""
	owner = models.OneToOneField(Account, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, unique=True, primary_key=True)
	description = models.TextField()

	def __str__(self):
		return self.name + ' : '+self.owner.name



class Banner(models.Model):
	uid = models.CharField(max_length=13, unique=True, primary_key=True)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	location = models.TextField()




class Product(models.Model):
	"""
	Doc here
	"""
	uid = models.CharField(max_length=18, unique=True, primary_key=True)
	title = models.CharField(max_length=30)
	price = models.FloatField()
	description = models.TextField()
	logo_url = models.TextField(default='Null')
	time_date = models.DateTimeField(auto_now=True)
	space = models.ForeignKey(Space, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
	in_stock = models.BooleanField(default=True)
	react_good = models.PositiveIntegerField(default=0)
	react_bad = models.PositiveIntegerField(default=0)
	react_fake = models.PositiveIntegerField(default=0)


class ProductReact(models.Model):
	"""
	Doc here
	"""
	uid = models.CharField(max_length=13, unique=True, primary_key=True)
	user = models.ForeignKey(Account, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	react = models.CharField(max_length=1, choices=_PRODUCT_REACT)



class ProductMedia(models.Model):
	"""
	Doc here
	"""
	uid = models.CharField(max_length=13, default='NULL')
	location = models.TextField(unique=True,primary_key=True)
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


class Sell(models.Model):
	"""
	Doc here
	"""
	uid = models.CharField(max_length=32, primary_key=True)
	by = models.ForeignKey(Space, on_delete=models.CASCADE)
	to = models.ForeignKey(Account, null=True, blank=True,on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
	time_date = models.DateTimeField(auto_now=True)