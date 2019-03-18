from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db import models


_GENDER = (
	('F', 'Female'),
	('M', 'Male'),
	('O', 'Other')
)


class UserManager(BaseUserManager):
	"""
	Doc here
	"""
	def create_user(self, phone, name, gender, password=None, is_staff=False, is_admin=False):

		if not phone or not name:
			raise ValueError('name and phone number required')


		if not password:
			raise ValueError('password required')


		user = self.model(phone=phone, name=name, gender=gender)
		user.is_staff = is_staff
		user.is_admin = is_admin
		user.set_password(password)
		user.save()

		return user


	def create_staffuser(self, phone, name, gender, password=None):
		user = self.create_user(phone, name, gender, password, True, False)
		return user


	def create_superuser(self, phone, name, gender, password=None):
		user = self.create_user(phone, name, gender, password, True, True)



class Account(AbstractBaseUser):
	"""
	Doc here
	"""
	phone = models.CharField(max_length=12, unique=True, primary_key=True)
	name = models.CharField(max_length=80)
	gender = models.CharField(max_length=1, choices=_GENDER)
	email = models.EmailField(max_length=45)
	thumbnail = models.TextField(default='https://i.postimg.cc/0N8mRzvP/user.png')

	has_space = models.BooleanField(default=False)
	has_notification = models.BooleanField(default=False)
	
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['name', 'gender']

	objects = UserManager()

	def __str__(self):
		return self.name + ': '+self.phone

	def get_username(self):
		return self.phone


	def has_perm(self, perm, obj=None):
		if self.is_admin:
			return True
		return False


	def has_module_perm(self, app_label):
		if self.is_admin:
			return True
		return False

	def has_module_perms(self, perms, obj=None):
		return all(self.has_perm(perm, obj) for perm in perms)
