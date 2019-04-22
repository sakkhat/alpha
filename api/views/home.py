from api.handler.tokenization import decode as token_decode
from api.serializer_models.home import (NotificationSerializer,PinnedProductSerializer,
	FavoriteSpaceSerializer)

from home.models import PinnedProduct, Notification, Favorite, _NOTIFICATION_LABEL_DIC

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def user_notification_list(request, format=None):
	token = request.GET.get('token', None)
	query = request.GET.get('query', None)

	if token is None:
		raise NotFound('request not found')

	data = token_decode(token)
	if data is None:
		raise NotFound('invalid request')

	user_id = data['user_id']
	if request.user.id != user_id:
		PermissionDenied('access denied')

	if query is None:
		raise NotFound('request not found')

	query = query.lower()
	result = None

	if query == 'all':
		result = Notification.objects.filter(user_id=user_id).order_by('-time_date')

	else:
		label = _NOTIFICATION_LABEL_DIC.get(query, None)
		if label is not None:
			result = Notification.objects.filter(user_id=user_id).filter(label=label
				).order_by('-time_date')


	if result is None:
		raise NotFound('request not found')
		
	serializer = NotificationSerializer(result, many=True)
	return Response(serializer.data)




@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def user_favorite_space_list(request, format=None):
	token = request.GET.get('token', None)
	if token is None:
		NotFound('invalid request')

	data = token_decode(token)
	if data is None:
		NotFound('invalid request')

	user_id = data['user_id']
	if user_id != request.user.id:
		PermissionDenied('access denied')

	result = Favorite.objects.filter(user=request.user).order_by('-time_date')
	serializer = FavoriteSpaceSerializer(result, many=True)
	return Response(serializer.data)




@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def user_pinned_product_list(request, format=None):

	token = request.GET.get('token', None)
	if token is None:
		raise NotFound('request not found')

	data = token_decode(token)
	if data is None:
		raise NotFound('invalid request')

	user_id = data['user_id']
	if request.user.id != user_id:
		raise PermissionDenied('access denied')

	result = PinnedProduct.objects.filter(user_id=user_id).order_by('-time_date')
	serializer = PinnedProductSerializer(result, many=True)
	return Response(serializer.data)
