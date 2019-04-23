from api.handler.tokenization import encode as token_encode

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from generic.variables import now_str


def verify_email(request, user):

	current_site = get_current_site(request)
	context = {
		'user' : user,
		'domain' : current_site.domain,
		'token' : token_encode({'user_id': user.id, 'email': user.email })
	}

	message = render_to_string('generic/mail/verify_email.html', context)
	mail = EmailMessage(subject='Sakkhat Verification', body=message, to=[user.email])
	mail.send()
