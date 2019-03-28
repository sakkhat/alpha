from api.handler import activity

from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class FavoriteRequestView(APIView):
	permission_classes = (IsAuthenticated,)
	
	def get(self, request, name, format=None):
		req = request.GET.get('req', None)
		if req is not None:
			res = activity.handle_favorite(request.user, name, req)
			if res:
				return Response({'response' : 'request accepted'})

		raise NotFound('request not found')