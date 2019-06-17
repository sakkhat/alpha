from django import template
from django.template import Template

register = template.Library()

@register.filter(name='gender')
def decode_gender(code):
    if code == 'M':
    	return 'Male'
    elif code == 'F':
    	return 'Female'
    elif code == 'O':
    	return 'Other'
    else:
    	return 'Not to say'


@register.filter(name='total_reacts')
def get_total_react(status):
	return status.total_good_react+status.total_bad_react+status.total_fake_react