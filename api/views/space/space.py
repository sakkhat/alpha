from api.handler import activity
from api.handler.tokenization import decode as token_decode
from api.serializer_models.space.space import SpaceStatusSerializer

from django.contrib.postgres.search import SearchVector

from generic.variables import SPACE_PAGINATION_SIZE

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
	
	if not result:
		raise NotFound('request not found')

	return Response({'response' : 'space added to favorite list'})


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def manager(request, format=None):

	token = request.GET.get('token', None)
	query = request.GET.get('query', None)

	page = request.GET.get('page', None)
	limit = request.GET.get('limit', None)

	if token is None:
		raise NotFound('invalid request')
	data = token_decode(token)
	if data is None:
		raise NotFound('invalid request')

	serializer = None

	page = __clean_value(page)
	limit = __clean_value(limit)

	if query is not None:
		serializer = __query_filter(query, page=page, limit=limit)

	else:
		if page is not None:
			offset = page * SPACE_PAGINATION_SIZE
			result = Status.objects.all().order_by('-space_id')[offset:offset+SPACE_PAGINATION_SIZE]
		else:
			result = Status.objects.all().order_by('-space_id')
		serializer = SpaceStatusSerializer(result, many=True)


	if serializer:
		return Response(serializer.data)
	

	raise NotFound('invalid request')




def __clean_value(value):
	if value is not None:
		if value.isdigit():
			return abs(int(value))

	return None



def __query_filter(query, **kwargs):
	query = query.lower()

	page = kwargs.get('page', None)
	limit = kwargs.get('limit', None)

	if page is None:
		return None

	if query == 'top':

		offset = page * SPACE_PAGINATION_SIZE
		result = Status.objects.order_by('-rating')[offset:offset+SPACE_PAGINATION_SIZE]
		serializer = SpaceStatusSerializer(result, many=True)
		return serializer

	elif len(query) > 0:

		offset = page*SPACE_PAGINATION_SIZE	
		result = Status.objects.annotate(search=SearchVector('space__name', 
			'space__description')).filter(search=query)[offset:offset+SPACE_PAGINATION_SIZE]
		
		serializer = SpaceStatusSerializer(result, many=True)
		return serializer

	return None