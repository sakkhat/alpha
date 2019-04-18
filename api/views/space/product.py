from account.models import Account

from api.serializer_models.space.product import ( ProductSerializer, ProductReactSerializer,
	ProductSerializerForReact)
from api.serializer_models.home import PinnedProductDetailSerializer
from api.handler import activity
from api.handler.tokenization import decode as token_decode

from django.core.exceptions import ObjectDoesNotExist

from home.models import PinnedProduct

from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from space.models import Product, ProductReact, Category
from space.models import _PRODDUCT_CATEGORY_KEY_DIC as category_key



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def product_react_list(request, format=None):
	token = request.GET.get('token', None)
	if token is None:
		raise NotFound('invalid request')
	data = token_decode(token)
	if data is None:
		raise NotFound('invalid request')
	user_id = data['user_id']
	result = ProductReact.objects.filter(user_id=user_id).order_by('-time_date')
	serializer = ProductReactSerializer(result, many=True)
	return Response(serializer.data)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def product_react_request(request, uid, format=None):
	token = request.GET.get('token', None)
	what = request.GET.get('react', None)
	if token is None:
		raise NotFound('request not found')

	data = token_decode(token)
	if data is None:
		raise None('invalid request')

	user_id = data['user_id']
	if request.user.id != user_id:
		PermissionDenied('access denied')

	if what is None:
		try:
			result = Product.objects.get(uid=uid)
			serializer = ProductSerializerForReact(result)
			return Response(serializer.data)
		except ObjectDoesNotExist as e:
			raise NotFound('request not found') 

	result = activity.handle_react(request.user, uid , what)
	if result is None:
		raise NotFound('request not found')

	serializer = ProductSerializerForReact(result)
	return Response(serializer.data)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def product_pinned_request(request, uid, format=None):
	token = request.GET.get('token', None)
	req = request.GET.get('req', None)
	if token is None:
		raise NotFound('request not found')

	data = token_decode(token)
	if data is None:
		raise None('invalid request')

	user_id = data['user_id']
	if request.user.id != user_id:
		PermissionDenied('access denied')

	req = req.upper()
	result = activity.handle_pin(request.user, uid, req)
	if result is None:
		raise NotFound('request not found')

	return Response({'response' : 'product pinned'});



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def manager(request, format=None):
	token = request.GET.get('token', None)
	if token is None:
		raise NotFound('invalid request')
	data = token_decode(token)
	if data is None:
		raise NotFound('invalid request')

	category = request.GET.get('category', None)
	query = request.GET.get('query', None)
	pinned_by = request.GET.get('pinned_by', None)
	limit = request.GET.get('limit', None)

	if limit is not None:
		if limit.isdigit():
			limit = int(limit)
		else:
			limit = None

	serializer = None

	if category is not None:
		serializer = __category_filter(category, limit)
			
		
	elif query is not None:
		serializer = __query_filter(query, limit)


	elif pinned_by is not None:
		serializer = __user_pinned_filter(data['user_id'], limit, request)


	if serializer:
		return Response(serializer.data)

	raise NotFound('invalid request')




def __category_filter(category, limit=None, request=None):
	try:
		category = category.lower()
		key = category_key.get(category)
		category_obj = Category.objects.get(name__iexact=key)
		if limit:
			result = Product.objects.filter(category_id=category_obj.id)[:limit]
		else:
			result = Product.objects.filter(category_id=category_obj.id)
		serializer = ProductSerializer(result, many=True)
		return serializer

	except ObjectDoesNotExist as e:
		return None



def __user_pinned_filter(user_id, limit=None, request=None):
	try:
		user = Account.objects.get(id=user_id)
		if request.user.id != user.id:
			raise PermissionDenied('access denied')
		result = PinnedProduct.objects.filter(user_id=user_id)
		serializer = PinnedProductDetailSerializer(result, many=True)
		return serializer

	except ObjectDoesNotExist as e:
		return None



def __query_filter(query, limit=None, request=None):
	query = query.lower()

	if query == 'trending':
		result = Product.objects.order_by('-time_date').order_by('-react_good')[:32]
		serializer = ProductSerializer(result, many=True)
		return serializer

	return None