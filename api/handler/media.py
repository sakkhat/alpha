from account.models import Account

from api.handler.tokenization import decode as token_decode

from django.core.exceptions import ObjectDoesNotExist

from generic.constants import (FILE_CHUNK_SIZE,PRODUCTS_FILE_PATH,USER_THUMBNAIL_PATH,
	SPACE_BANNER_PATH)
from generic.media import Image as ImageHandler

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import NotFound,PermissionDenied, NotAcceptable
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from space.models import Space, Product, ProductMedia, Banner



@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def update(request):

	put_data = request.data

	token = put_data.get('token', None)
	if token is None:
		return invalid_request(request)
	token_data = token_decode(token)

	user = request.user
	if user.id != token_data['user_id']:
		raise PermissionDenied('access permission denied')


	what = put_data.get('what', None)
	uid = put_data.get('current', None)
	space_name = put_data.get('space', None)

	file = put_data.get('image', None)
	if file is None:
		raise NotFound('invalid request')
	
	if not ImageHandler.is_valid_format(file.name):
		raise NotAcceptable('unacceptable type of file')

	if what is None:
		raise NotFound('invalid request')
	what = what.lower()

	if what == 'banner':
		if uid is None:
			raise NotFound('invalid request')
		if space_name is None:
			raise NotFound('invalid request')
		return _update_banner(user, uid, space_name, file)

	elif what == 'product':
		if uid is None:
			raise NotFound('invalid request')
		if space_name is None:
			raise NotFound('invalid request')
		return _update_product_media(user, uid, space_name, file)

	elif what == 'account':
		return _update_account_thumbnail(user, file)



def _update_banner(user, uid, space_name, file):
	try:
		banner = Banner.objects.get(uid=uid)
		space = Space.objects.get(name__iexact=space_name)

		if space.owner_id != user.id:
			raise PermissionDenied('access permission denied')

		if banner.space_id != space.id:
			raise PermissionDenied('access permission denied')

		img_src = ImageHandler.load(file_stream=file)
		img_path = ImageHandler.save(SPACE_BANNER_PATH, img_src)
		ImageHandler.delete(banner.location)
		banner.location = img_path
		banner.save()

		return Response({'image' : img_path})

	except ObjectDoesNotExist as e:
		raise NotFound('invalid request')



def _update_product_media(user, uid, space_name, file):
	try:
		product_media = ProductMedia.objects.get(uid=uid)
		product = Product.objects.get(uid=product_media.product_id)
		space = Space.objects.get(name__iexact=space_name)

		if product.space_id != space.id:
			raise PermissionDenied('access permission denied')

		img_src = ImageHandler.load(file_stream=file)
		img_path = ImageHandler.save(PRODUCTS_FILE_PATH, img_src)

		if product.logo_url == product_media.location:
			product.logo_url = img_path
			product.save()

		ImageHandler.delete(product_media.location)
		product_media.location = img_path
		product_media.save()

		return Response({'image' : img_path})

	except ObjectDoesNotExist as e:
		raise NotFound('invalid request')



def _update_account_thumbnail(user, file):
	img_src = ImageHandler.load(file_stream=file)
	img_path = ImageHandler.save(USER_THUMBNAIL_PATH, img_src)
	ImageHandler.delete(user.thumbnail)
	user.thumbnail = img_path
	user.save()

	return Response({'image' : img_path })