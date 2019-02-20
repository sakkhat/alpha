from django import forms

from account.models import Account

from .models import Space,Product


class SpaceCreateForm(forms.ModelForm):
	logo = forms.FileInput(attrs=
		{})

	cover = forms.FileInput(attrs=
		{})

	class Meta:
		model = Space
		fields = ['name', 'descriptions','category']




class ProductPostForm(forms.ModelForm):

	class Meta:
		model = Product

