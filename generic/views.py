from django.shortcuts import HttpResponse,render
from django.template import loader

from json import dumps as _json_maker


def response(request, template_name, context={}):
	html = loader.get_template(template_name)
	return HttpResponse(html.render(context, request))


def invalid_request(request, context={}):
	return render(request, 'generic/invalid_request.html', context)



def json_response(request, context={}, json_data=None):
	result = _json_maker({"data":json_data})
	return HttpResponse(result)