from django import forms


class PasswordConfirmForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput(attrs=
		{'minLength' : '6', 'class' : 'form-control', 'placeholder' : 'account password'}))

	def clean_password(self):
		password = self.cleaned_data['password']
		valid = self.user.check_password(password)
		if not valid:
			raise forms.ValidationError('invalid password')
		return password

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PasswordConfirmForm, self).__init__(*args, **kwargs)