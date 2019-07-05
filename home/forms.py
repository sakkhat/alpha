from django import forms
from home.models import Feedback

class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Feedback
		fields = ['body', 'email']
		widgets = {
			'body' : forms.Textarea(attrs={
					'placeholder': 'Your feedback in 250 characters',
					'maxLength' : '250', 'class' : 'form-control'
				}),
			'email' : forms.EmailInput(attrs={
					'placeholder' : 'Your email address',
					'class' : 'form-control'
				})
		}

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(FeedbackForm, self).__init__(*args, **kwargs)
		if self.user.is_authenticated:
			self.fields['userS'].initial = self.user.email


	def save(self, commit=True):
		obj = super(FeedbackForm, self).save(commit=False)
		if commit:
			obj.save()
		return obj
