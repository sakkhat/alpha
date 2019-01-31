from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
	
	def create_user(self, id_name, password, display_name, is_staff=False,  is_admin=False):
		
		if not id_name:
			raise ValueError('Insert ID name')

		if not password:
			raise ValueError('Insert password')

		if not display_name:
			raise ValueError('Insert display name')

		user = self.model(id_name = id_name)
		user.display_name = display_name
		user.is_staff = is_staff
		user.is_admin = is_admin

		user.set_password(password)
		user.save()

		return user


	def create_superuser(self, id_name, password):
		if not id_name or password:
			raise ValueError('Fill up fields')

		return self.create_user(id_name, password, 'Admin Account', True, True)
		


	def create_staffuser(self, id_name, password):
		if not id_name or password:
			raise ValueError('Fill up fields')

		return  self.create_user(id_name, password, 'Staff Account', True, False)


class Account(AbstractBaseUser):
	id_name = models.CharField(max_length=30, unique = True)
	phone = models.CharField(max_length=12, unique=True, primary_key=True)
	display_name = models.CharField(max_length=50)

	USERNAME_FIELD = 'id_name'
	REQUIRED_FIELDS = ['phone', 'display_name']

	is_admin = models.BooleanField(default = False)
	is_staff = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)

	objects = UserManager()

	def get_username(self):
		return self.id_name

	def __str__(self):
		return self.id_name



class Profile(models.Model):
	"""
	description
	thumbnail 
	logo
	cover
	category
	address
	location_zone
	"""

	description = models.TextField()
	# location
	thumbnail = models.CharField(max_length=100) 
	logo = models.CharField(max_length=100)
	cover = models.CharField(max_length=100)
	address = models.CharField(max_length=30)
	location_zone = models.CharField(max_length = 5)
	user = models.OneToOneField(Account, on_delete=models.CASCADE)



class Post(models.Model):
	"""
	"""
	price = models.FloatField()
	description = models.TextField()
	time_date = models.DateTimeField(auto_now=now)
	user = models.OneToOneField(Account, on_delete=models.CASCADE)


class PostMedia(models.Model):
	"""
	"""
	location = models.CharField(max_length=100)
	is_image = models.BooleanField(default=True)
	post = models.OneToOneField(Post, on_delete=models.CASCADE)