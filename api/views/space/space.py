from api.handler import activity
from api.handler.tokenization import decode as token_decode
from api.serializer_models.space.space import SpaceStatusSerializer

from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from space.models import Status



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def favorite_request(request, name, format=None):
	token = request.GET.get('token', None)
	req = request.GET.get('req', None)

	if token is None:
		raise NotFound('invalid request')
	data = token_decode(token)
	if data is None:
		raise NotFound('invalid request')

	if req is None:
		raise NotFound('request not found')
	
	result = activity.handle_favorite(request.user, name, req)
	if result is None:
		raise NotFound('request not found')

	return Response({'response' : 'space added to favorite list'})


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def manager(request, format=None):
	token = request.GET.get('token', None)
	req = request.GET.get('req', None)

	if token is None:
		raise NotFound('invalid request')
	data = token_decode(token)
	if data is None:
		raise NotFound('invalid request')

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