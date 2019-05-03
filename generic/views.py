from django.shortcuts import HttpResponse,render
from django.template import loader

from generic.forms import PasswordConfirmForm

from json import dumps as _json_maker


def response(request, template_name, context={}):
	html = loader.get_template(template_name)
	return HttpResponse(html.render(context, request))


def invalid_request(request, context={}):
	return render(request, 'generic/views/error404.html', context, status=404)


def error500(request, context={}):
	return render(request, 'generic/views/error500.html', context, status=500)


def json_response(request, context={}, json_data=None):
	result = _json_maker({"data":json_data})
	return HttpResponse(result)


def password_confirmation(request, context):
	print(context)
	return render(request, 'generic/views/password_confirmation.html', context)