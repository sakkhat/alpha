from django.core.mail import send_mail
from django.conf import settings
from django import forms


class FeedbackForm(forms.Form):
	body = forms.CharField(widget=forms.Textarea(attrs=
		{'class':'form-control', 'placeholder': 'Your feedback message'}))
	sender = forms.CharField(widget=forms.EmailInput(attrs=
		{'class':'form-control', 'placeholder' : 'example@mail.com'}))



	def send(self):
		body = self.cleaned_data['body']
		sender = self.cleaned_data['sender']

		send_mail(
			subject = 'Sakkhat Feedback',
			message = body+'\n'+sender,
			from_email = settings.EMAIL_HOST_USER,
			recipient_list = [settings.EMAIL_HOST_USER],
			fail_silently = True
		)

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(FeedbackForm, self).__init__(*args, **kwargs)

		if self.user.is_authenticated:
			self.fields['sender'].initial = self.user.email
