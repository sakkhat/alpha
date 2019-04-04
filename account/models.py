from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager,PermissionsMixin, 
	_user_has_module_perms, _user_has_perm, _user_get_all_permissions)
from django.db import models

from uuid import uuid4


_GENDER = (
	('F', 'Female'),
	('M', 'Male'),
	('O', 'Other'),
	('*', 'Not to say'),
)


class UserManager(BaseUserManager):
	"""
	Doc here
	"""
	def create_user(self, phone, name, email, gender, password=None, is_staff=False, is_superuser=False):

		if not phone or not name or not email:
			raise ValueError('name, phone, email required')

		if not password:
			raise ValueError('password required')


		user = self.model(phone=phone, name=name, email=email, gender=gender)
		user.is_staff = is_staff
		user.is_superuser = is_superuser
		user.set_password(password)
		user.save()

		return user


	def create_staffuser(self, phone, name, email, gender, password=None):
		user = self.create_user(phone, name, email, gender, password, True, False)
		return user


	def create_superuser(self, phone, name, email, gender, password=None):
		user = self.create_user(phone, name, email, gender, password, True, True)



class Account(AbstractBaseUser,PermissionsMixin):
	"""
	Doc here
	"""
	phone = models.CharField(max_length=11, unique=True)
	name = models.CharField(max_length=80)
	gender = models.CharField(max_length=1, choices=_GENDER)
	email = models.EmailField(max_length=45, unique=True)
	thumbnail = models.TextField(default='https://i.postimg.cc/Y2zkXSFB/user.png')

	has_space = models.BooleanField(default=False)
	has_notification = models.BooleanField(default=False)
	
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['name', 'email', 'gender']

	objects = UserManager()

	def __str__(self):
		return self.name + ': '+self.phone

	def get_username(self):
		return self.phone


	def has_perm(self, perm, obj=None):
		if self.is_superuser:
			return True
		return False


	def has_module_perm(self, app_label):
		if self.is_superuser:
			return True
		return False

	def has_module_perms(self, perms, obj=None):
		return all(self.has_perm(perm, obj) for perm in perms)
