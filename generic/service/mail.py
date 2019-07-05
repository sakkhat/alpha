from api.handler.tokenization import encode as token_encode

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def verify_email(request, user):
	current_site = get_current_site(request)
	context = {
		'user' : user,
		'domain' : current_site.domain,
		'token' : token_encode({'user_id': user.id, 'email': user.email })
	}

	message = render_to_string('generic/mail/verify_email.html', context)
	send_mail(subject='Sakkhat Verification', 
			message=message, 
			from_email=settings.EMAIL_HOST_USER,
			recipient_list = [user.email,])
