from django.db import models

# Create your models here.

# user account model
class Account(models.Model):
	dname = models.CharField(max_length = 80)
	sname = models.CharField(max_length = 80)
	email = models.CharField(max_length = 50)
	phone = models.CharField(max_length = 16)
	category = models.CharField(max_length = 30)
	password = models.CharField(max_length = 100)
	dimg = models.CharField(max_length = 1000)

	def __str__(self):
		return  self.sname +' : '+ self.dname

class Post(models.Model):
	ac = models.ForeignKey(Account, on_delete = models.CASCADE)
	title = models.CharField(max_length = 30)
	description = models.CharField(max_length = 150)
	icon = models.CharField(max_length = 1000)


