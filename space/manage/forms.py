from django import forms
from generic.media import Image
from generic.constants import FILE_CHUNK_SIZE, PRODUCTS_FILE_PATH, SPACE_LOGO_PATH
from space.models import Space, Banner



class SpaceCreateForm(forms.ModelForm):
	_UNUSABLE_NAMES = ['space','sakkhat','login','signin','signup','create','api','admin',
		'url', 'http', 'https','product','account','user','notification','page','account',
		'home','feed','trending','explore','search',]

	_UNUSABLE_SYMBOLS = [' ', '&', '*', '#', '@', '!', '+', '%', ':', ';','"', "'", ',','`','~','\\',
		'/','|','{','}','[',']','(',')','?','>','<','^']

	logo = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input','onchange':'openFile(event, "logo-view")',
		'accept':'.jpg, .png, .jpeg'}))

	logo_path = None

	class Meta:
		model = Space
		fields = ['name', 'display_name', 'description',]

		widgets = {
			'name' : forms.TextInput(attrs=
				{'placeholder':'Unique Name (max 20 char)', 'class':'form-control'}),
			'display_name' : forms.TextInput(attrs=
				{'placeholder':'Display Name (max 80 char)', 'class':'form-control'}),
			'description' : forms.Textarea(attrs=
				{'placeholder':'My description. Follow: https://facebook.com/sakkhat.inc/', 'class':'form-control'})
		}

	def clean_logo(self):
		logo = self.cleaned_data['logo']
		self.logo_path = Image.load_and_save(logo, SPACE_LOGO_PATH)
		if not self.logo_path:
			raise forms.ValidationError('invalid file input')
		print(logo)
		return logo

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
		space.logo = self.logo_path
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
		fields = ['name','display_name','description',]

		widgets = {
			'name' : forms.TextInput(attrs={'class':'form-control mb-2'}),
			'display_name' : forms.TextInput(attrs={'class':'form-control mb-2'}),
			'description' : forms.Textarea(attrs={'class':'form-control'})
		}


	def clean(self):
		cleaned_data = self.cleaned_data
		name = cleaned_data['name']

		query = Space.objects.filter(name__iexact=name).exclude(id=self.space.id).first()
		if query is not None:
			raise forms.ValidationError('space name already taken')
		return cleaned_data


	def save(self, commit=True):
		self.space.name = self.cleaned_data['name']
		self.space.display_name = self.cleaned_data['display_name']
		self.space.description = self.cleaned_data['description']
		if commit:
			self.space.save()
		return self.space

	def __init__(self, *args, **kwargs):
		self.space = kwargs.pop('space', None)
		super(SpaceUpdateForm, self).__init__(*args, **kwargs)
		self.fields['name'].initial = self.space.name
		self.fields['display_name'].initial = self.space.display_name
		self.fields['description'].initial = self.space.description