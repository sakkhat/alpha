from api.handler import activity
from api.serializer_models.space.space import SpaceStatusSerializer

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from space.models import Status


class FavoriteRequestView(APIView):
	permission_classes = (IsAuthenticated,)
	
	def get(self, request, name, format=None):
		req = request.GET.get('req', None)
		if req is not None:
			res = activity.handle_favorite(request.user, name, req)
			if res:
				return Response({'response' : 'request accepted'})

		raise NotFound('request not found')


@api_view(['GET'])
def manager(request, format=None):
	query = request.GET.get('query', None)

	if query is not None:
		query = query.lower()
		if query == 'top':
			limit = request.GET.get('limit', None)
			if limit is not None:
				if limit.isdigit():
					limit = int(limit)
					result = Status.objects.order_by('-rating')[:limit]
					serializer = SpaceStatusSerializer(result, many=True)
					return Response(serializer.data)

			result = Status.objects.order_by('-rating')[:32]
			serializer = SpaceStatusSerializer(result, many=True)
			return Response(serializer.data)

	result = Status.objects.all().order_by('-space_id')
	serializer = SpaceStatusSerializer(result, many=True)
	return Response(serializer.data)