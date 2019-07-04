from django.contrib.auth import authenticate
from django import forms

from account.models import Account


class SignupForm(forms.ModelForm):

	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Password (min 6 length)', 'class' : 'form-control', 'minLength': '6'}))

	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Confirm Password', 'class' : 'form-control'}))

	class Meta:
		model = Account
		fields = ['phone', 'name', 'email', 'gender']

		widgets = {
			'name' : forms.TextInput(attrs={
				'placeholder' : 'Rafiul Islam', 'class' : 'form-control'
				}),

			'phone' : forms.TextInput(attrs={
				'placeholder' : '01XXXXXXXXX', 'class' : 'form-control'
				}),

			'email' : forms.EmailInput(attrs={
				'placeholder' : 'example@mail.com', 'class' : 'form-control'
				}),

			'gender' : forms.Select(attrs={
				'class' : 'custom-select'
				}),
		}

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		query = Account.objects.filter(phone=phone).first()

		if query:
			raise forms.ValidationError('this phone already registered')

		return phone


	def clean_email(self):
		email = self.cleaned_data['email']
		query = Account.objects.filter(email__iexact=email).first()

		if query:
			raise forms.ValidationError('this email already taken')

		return email


	def clean_confirm_password(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password and confirm_password and password != confirm_password:
			raise forms.ValidationError("passwords doesn't matched")

		return confirm_password


	def save(self, commit=True):
		user = super(SignupForm,self).save(commit=False)
		user.set_password(self.cleaned_data['confirm_password'])
		if commit:
			user.save()
		return user



class SigninForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs=
		{'placeholder' : 'Email', 
		'class' : 'form-control'}))

	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Password', 
		'class' : 'form-control'}))


	def clean(self):
		cleaned_data = self.cleaned_data
		email = cleaned_data['email']
		password = cleaned_data['password']

		user = authenticate(email=email, password=password)
		if user:
			self.user = user
			return cleaned_data
		raise forms.ValidationError('invalid information')



class PasswordChangeForm(forms.Form):

	current_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Current Password', 'class' : 'form-control'}))
	new_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'New Password', 'class' : 'form-control', 'minLength':'6'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Confirm Password', 'class' : 'form-control'}))

	def clean_current_password(self):
		current_password = self.cleaned_data['current_password']
		isvalid = self.user.check_password(current_password)
		if not isvalid:
			raise forms.ValidationError('invalid password')
		return current_password

	def clean_confirm_password(self):
		new_password = self.cleaned_data['new_password']
		confirm_password = self.cleaned_data['confirm_password']

		if new_password and confirm_password and new_password != confirm_password:
			raise forms.ValidationError("New and Confirm Password doesn't matched")
		return confirm_password


	def save(self, commit=True):
		new_password = self.cleaned_data['confirm_password']
		self.user.set_password(new_password)
		if commit:
			self.user.save()
		return self.user


	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PasswordChangeForm, self).__init__(*args, **kwargs)



class ProfileUpdateForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'class' : 'form-control', 'placeholder' : 'Your Password'}))

	class Meta:
		model = Account
		fields = ['name', 'email', 'phone', 'gender']

		widgets = {
			'name' : forms.TextInput(attrs={
				'placeholder' : 'Name', 'class' : 'form-control'
				}),

			'email' : forms.EmailInput(attrs={
				'placeholder' : 'Email', 'class' : 'form-control'
				}),

			'phone' : forms.TextInput(attrs={
				'placeholder' : 'Phone', 'class' : 'form-control'
				}),

			'gender' : forms.Select(attrs={
				'class' : 'custom-select'
				}),
		}


	def clean(self):
		cleaned_data = self.cleaned_data

		password = cleaned_data['password']
		email = cleaned_data['email']
		phone = cleaned_data['phone']
		gender = cleaned_data['gender']

		valid = self.user.check_password(password)
		if not valid:
			raise forms.ValidationError('invalid password')

		duplicate_email = Account.objects.filter(email=email).exclude(id=self.user.id)
		if duplicate_email.exists():
			raise forms.ValidationError('This email is already registered')

		duplicate_phone = Account.objects.filter(phone=phone).exclude(id=self.user.id)
		if duplicate_phone.exists():
			raise forms.ValidationError('This phone is already registered')

		if gender is None:
			raise forms.ValidationError('set a gender')

		return cleaned_data


	def is_new_email(self):
		if self.user.email.lower() != self.cleaned_data.get('email').lower():
			return True
		return False


	def save(self, commit=True):
		name = self.cleaned_data['name']
		email = self.cleaned_data['email']
		phone = self.cleaned_data['phone']
		gender = self.cleaned_data['gender']

		self.user.name = name
		self.user.email = email
		self.user.phone = phone
		self.user.gender = gender

		if commit:
			self.user.save()
		return self.user


	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(ProfileUpdateForm, self).__init__(*args, **kwargs)		

		self.fields['name'].initial = self.user.name
		self.fields['email'].initial = self.user.email
		self.fields['phone'].initial = self.user.phone
		self.fields['gender'].initial = self.user.gender