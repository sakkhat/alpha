from account.models import Account

from api.serializer_models.account import AccountSerializerForThumbnail

from django.core.exceptions import ObjectDoesNotExist

from generic.media import Image
from generic.variables import USER_THUMBNAIL_PATH


from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.response import Response



@api_view(['GET', 'POST', 'PUT'])
def user_thumbnail_update(request, ac_id):

	if not request.user.is_authenticated:
		raise PermissionDenied('no permission')

	if request.user.phone != ac_id:
		raise NotFound('request not found')

	if request.method == 'PUT':
		try:
			
			file = request.FILES['image']
			print(file.name)
			print(type(file))
			img_src = Image.load(file_stream=file)

			try:
				user = Account.objects.get(phone=ac_id)
				img_path = Image.save(USER_THUMBNAIL_PATH, img_src)

				Image.delete(user.thumbnail)
			

				user.thumbnail = img_path
				user.save()

				serializer = AccountSerializerForThumbnail(user)
				return Response(serializer.data)


			except ObjectDoesNotExist as e:
				pass

		except Exception as e:
			pass
	
	raise NotFound('request not found')