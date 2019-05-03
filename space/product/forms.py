from django import forms
from generic.media import Image
from generic.constants import FILE_CHUNK_SIZE, PRODUCTS_FILE_PATH
from space.models import Product, ProductMedia, Space



class ProductPostForm(forms.ModelForm):
	img1 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input','onchange':'openFile(event, "img-view-1")'}))

	img2 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input','onchange':'openFile(event, "img-view-2")'}))

	img3 = forms.ImageField(widget=forms.FileInput(attrs=
		{'class':'custom-file-input','onchange':'openFile(event, "img-view-3")'}))

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
