from django import forms
from generic.media import Image
from generic.constants import FILE_CHUNK_SIZE, PRODUCTS_FILE_PATH
from space.models import Space, Banner



class SpaceCreateForm(forms.ModelForm):
	_UNUSABLE_NAMES = ['space','sakkhat','login','signin','signup','auth','web','create','api',
		'url', 'http', 'https','product','account','user','all','notification']

	_UNUSABLE_SYMBOLS = [' ', '&', '*', '#', '@', '!', '+', '%', ':', ';','"', "'", ',','`','~','\\',
		'/','|','{','}','[',']','(',')','?','>','<','^']

	class Meta:
		model = Space
		fields = ['name', 'description',]

		widgets = {
			'name' : forms.TextInput(attrs=
				{'placeholder':'Sakkhat', 'class':'form-control'}),
			'description' : forms.Textarea(attrs=
				{'placeholder':'My description. Follow: https://facebook.com/sakkhat.inc/', 'class':'form-control'})
		}


	def clean_name(self):
		name = self.cleaned_data['name']
		
		for i in self._UNUSABLE_SYMBOLS:
			if i in name:
				raise forms.ValidationError(i+ "is invalid")

		for i in self._UNUSABLE_NAMES:
			if i.lower() == name.lower():
				raise forms.ValidationError('Restricted Name')

		query = Space.objects.filter(name__iexact=name).first()
		if query:
			raise forms.ValidationError('Space name already taken')

		return name



	def save(self, commit=True):
		space = super(SpaceCreateForm, self).save(commit=False)
		space.owner = self.request.user
		if commit:
			space.save()

			banner1 = Banner(space=space)
			banner2 = Banner(space=space)
			banner3 = Banner(space=space)

			banner1.save()
			banner2.save()
			banner3.save()

			
		return space


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(SpaceCreateForm, self).__init__(*args, **kwargs)


class SpaceUpdateForm(forms.ModelForm):
	class Meta:
		model = Space
		fields = ['description',]

		widgets = {
			'description' : forms.Textarea(attrs=
				{'placeholder':'Description', 'class':'form-control'})
		}

	def __init__(self, *args, **kwargs):
		self.space = kwargs.pop('space', None)

		super(SpaceUpdateForm, self).__init__(*args, **kwargs)
		
		self.fields['description'].initial = self.space.description