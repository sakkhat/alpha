from django import forms

from .models import Account

class LoginForm(forms.Form):
	user_id = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
			'placeholder' : 'ID Name or Phone'
		}))

	password = forms.CharField(widget=forms.PasswordInput(
		attrs= {'placeholder' : 'Password'}))




class RegistrationForm(forms.Form):
	id_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
		'placeholder' : 'ID Name', 'pattern': '^[a-zA-Z][a-zA-Z0-9-_\.]{1,30}$'}))

	phone = forms.CharField(max_length=12, widget=forms.TextInput(attrs={
		'placeholder' : 'Phone Number', 'pattern' : '[0-9]+'}))

	password1 = forms.CharField(widget=forms.PasswordInput(attrs={
		'minlength' : '6', 'placeholder' : 'Password'}))

	password2 = forms.CharField(widget=forms.PasswordInput(attrs={
		'minlength' : '6', 'placeholder' : 'Confirm Password'}))


	display_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
		'placeholder' : 'Display Name'}))


	description = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder' : 'Short Description'}))


	address = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
		'placeholder' : 'Address'}))


	def clean_id_name(self):
		id_name = self.cleaned_data['id_name']
		query = Account.objects.filter(id_name = id_name)

		if query.exists():
			raise forms.ValidationError('ID name already exists')

		return id_name


	def clear_phone(self):
		phone = self.cleaned_data['phone']
		query = Account.objects.filter(phone = phone)

		if query.exists():
			raise forms.ValidationError('Phone number already exists')

		return phone

	
	def clean_password2(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']

		if password1 and password2 and password1 is not password2:
			raise forms.ValidationError('Password not matched')

		return password2