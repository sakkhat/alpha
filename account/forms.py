from django.contrib.auth import authenticate
from django import forms

from account.models import Account

class SignupForm(forms.ModelForm):

	password1 = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Password'}))

	password2 = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Confirm Password'}))

	class Meta:
		model = Account
		fields = [
			'name', 'phone', 'gender','email'
		]

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		query = Account.objects.filter(phone=phone)

		if query.exists():
			raise forms.ValidationError('this phone already registered')

		return phone

	def clean_password2(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']

		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("passwords doesn't matched")

		return password2


	def save(self, commit=True):
		user = super(SignupForm,self).save(commit=False)
		user.set_password(self.cleaned_data['password2'])
		if commit:
			user.save()
		return user


	widgets = {
		'name' : forms.TextInput(attrs={
			'placeholder' : 'Name',
			}),

		'phone' : forms.TextInput(attrs={
			'placeholder' : 'Phone',
			}),

		'email' : forms.EmailInput(attrs={
			'placeholder' : 'Email (optional)'
			}),

		'gender' : forms.Select(attrs={

			}),
	}

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(args, kwargs)
		self.fields['email'].required = False


class SigninForm(forms.Form):
	phone = forms.CharField(max_length=12, widget=forms.TextInput(attrs=
		{'placeholder' : 'Phone'}))

	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Password'}))


class PasswordChangeForm(forms.Form):

	current_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Current Password'}))
	new_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'New Password'}))
	confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Confirm Password'}))

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


class PasswordResetForm(forms.Form):
	password1 = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'New Password'}))

	password2 = forms.CharField(widget=forms.PasswordInput(attrs=
		{'placeholder' : 'Confirm Password'}))



