from account.models import Account

from rest_framework.serializers import ModelSerializer

class AccountSerializerForThumbnail(ModelSerializer):
	class Meta:
		model = Account
		fields = ('thumbnail',)
