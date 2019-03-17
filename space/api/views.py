from django.core.exceptions import ObjectDoesNotExist

from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from space.api.serializer import BannerSerializer
from space.models import Banner


import urllib.request

class SpaceBanner(ListAPIView):
	serializer_class = BannerSerializer

	def get(self, request, format=None):
		queryset = Banner.objects.all()
		return Response(queryset)


	def post(self, request, format=None):

		body = request.body
		print(len(body))

		queryset = Banner.objects.all()
		return Response(queryset)
