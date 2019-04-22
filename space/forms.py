from django import forms

from generic.variables import FILE_CHUNK_SIZE, PRODUCTS_FILE_PATH
from generic.media import Image

from space.models import Space,Product, ProductMedia,Banner



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
				{'placeholder':'My description. Follow: https://facebook.com/sakkhat/', 'class':'form-control'})
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
		



class ProductPostForm(forms.ModelForm):
	img1 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input','onchange':'openFile1(event)'}))

	img2 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input','onchange':'openFile2(event)'}))

	img3 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input','onchange':'openFile3(event)'}))

	preview_select = forms.ChoiceField(
		choices=((1, 'Image 1'), (2, 'Image 2'), (3, 'Image 3')),
		widget=forms.Select({'class':'form-control'}))

	img1_path = None
	img2_path = None
	img3_path = None
	logo_url = None

	class Meta:
		model = Product
		fields = ['title', 'description', 'category', 'price', 'phone_request',
			'email_request',
		]

		widgets = {
			'title' : forms.TextInput(attrs=
				{'placeholder':'Product Name (max 30 character)', 'class':'form-control'}),
			'description' : forms.Textarea(attrs=
				{'placeholder':'Product Description', 'class':'form-control'}),

			'price' : forms.NumberInput(attrs=
				{'placeholder':'(TK)', 'class':'form-control'}),
			'category' : forms.Select(attrs=
				{'class':'form-control'}),
			'phone_request' : forms.CheckboxInput(attrs=
				{'class':'custom-control-input'}),
			'email_request' : forms.CheckboxInput(attrs=
				{'class':'custom-control-input'}),
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

		if commit:

			preview_select = self.cleaned_data['preview_select']

			if preview_select == '1':
				post.logo_url = self.img1_path
			elif preview_select == '2':
				post.logo_url = self.img2_path
			else:
				post.logo_url = self.img3_path




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




class ProductUpdateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['title', 'description', 'price', 'category', 'in_stock',
			'phone_request', 'email_request',
		]

		widgets = {
			'title' : forms.TextInput(attrs=
				{'placeholder':'Title', 'class':'form-control'}),
			'description' : forms.Textarea(attrs=
				{'placeholder':'Description', 'class':'form-control'}),

			'price' : forms.NumberInput(attrs=
				{'placeholder':'Price (TK)', 'class':'form-control'}),
			'category' : forms.Select(attrs=
				{'class':'form-control'}),
			'in_stock' : forms.CheckboxInput(attrs=
				{'class' : 'custom-control-input'}),
			'phone_request' : forms.CheckboxInput(attrs=
				{'class':'custom-control-input'}),
			'email_request' : forms.CheckboxInput(attrs=
				{'class':'custom-control-input'}),
		}


	def clean_category(self):
		category = self.cleaned_data['category']
		if category is None:
			raise forms.ValidationError('product must have a category')
		else:
			return category


	def __init__(self, *args, **kwargs):
		self.product = kwargs.pop('product', None)

		super(ProductUpdateForm, self).__init__(*args, **kwargs)
		
		self.fields['title'].initial = self.product.title
		self.fields['description'].initial = self.product.description
		self.fields['price'].initial = self.product.price
		self.fields['category'].initial = self.product.category
		self.fields['in_stock'].initial = self.product.in_stock
		self.fields['phone_request'].initial = self.product.phone_request
		self.fields['email_request'].initial = self.product.email_request
