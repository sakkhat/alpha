from django import forms

from generic.variables import now_str, FILE_CHUNK_SIZE, PRODUCTS_FILE_PATH
from generic.media import Image

from space.models import Space,Product, ProductMedia



class SpaceCreateForm(forms.ModelForm):
	_UNUSABLE_NAMES = ['space','sakkhat','login','signin','signup','auth','web','create','api',\
		'url', 'http', 'https','product','account','user']

	_UNUSABLE_SYMBOLS = [' ', '&', '*', '#', '@', '!', '+', '%', ':', ';','"', "'", ',','`','~','\\',
		'/','|','{','}','[',']','(',')','?','>','<','^']

	class Meta:
		model = Space
		fields = ['name', 'description',]

		widgets = {
			'name' : forms.TextInput(attrs=
				{'placeholder':'Space Name', 'class':'form-control'}),
			'description' : forms.Textarea(attrs=
				{'placeholder':'Description', 'class':'form-control'})
		}


	def clean_name(self):
		name = self.cleaned_data['name']
		
		for i in self._UNUSABLE_SYMBOLS:
			if i in name:
				raise forms.ValidationError(i+ "is invalid")

		for i in self._UNUSABLE_NAMES:
			if i.lower() == name.lower():
				raise forms.ValidationError('Restricted Name')

		query = Space.objects.filter(name=name)
		if query.exists():
			raise forms.ValidationError('Space name already taken')

		return name



	def save(self, commit=True):
		space = super(SpaceCreateForm, self).save(commit=False)
		space.owner = self.request.user
		if commit:
			space.save()
		return space


	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(SpaceCreateForm, self).__init__(*args, **kwargs)
		



class ProductPostForm(forms.ModelForm):
	img1 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input'}))

	img2 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input'}))

	img3 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input'}))

	img1_path = None
	img2_path = None
	img3_path = None
	logo_url = None

	class Meta:
		model = Product
		fields = ['title', 'description', 'category', 'price']

		widgets = {
			'title' : forms.TextInput(attrs=
				{'placeholder':'Title', 'class':'form-control'}),
			'description' : forms.Textarea(attrs=
				{'placeholder':'Description', 'class':'form-control'}),

			'price' : forms.NumberInput(attrs=
				{'placeholder':'Price (TK)', 'class':'form-control'}),
			'category' : forms.Select(attrs=
				{'class':'form-control'})
		}


	def load_images(self):
		img1 = self.cleaned_data['img1']
		img2 = self.cleaned_data['img2']
		img3 = self.cleaned_data['img3']

		img1_file = Image.load(file_stream=img1)
		img2_file = Image.load(file_stream=img2)
		img3_file = Image.load(file_stream=img3)

		self.img1_path = Image.save(PRODUCTS_FILE_PATH, img1_file)
		self.img2_path = Image.save(PRODUCTS_FILE_PATH, img2_file)
		self.img3_path = Image.save(PRODUCTS_FILE_PATH, img3_file)


	def save(self, commit=True):
		post = super(ProductPostForm, self).save(commit=False)
		space = Space.objects.get(owner = self.request.user)
		post.space = space
		post.uid = now_str(mul=6)
		if commit:
			post.logo_url = self.img1_path
			post.save()

			media1 = ProductMedia(location=self.img1_path, product=post)
			media2 = ProductMedia(location=self.img2_path, product=post)
			media3 = ProductMedia(location=self.img3_path, product=post)
			
			media1.save()
			media2.save()
			media3.save()

		return post



	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(ProductPostForm, self).__init__(*args, **kwargs)


