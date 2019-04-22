from django.conf import settings

from jwt import decode as __decode
from jwt import encode as __encode
from jwt.exceptions import InvalidTokenError


def decode(token):
	try:
		data = __decode(token, settings.SECRET_KEY, algorithms=['HS256'])
		return data
	except InvalidTokenError as e:
		return None


def encode(data):
	token = __encode(data, settings.SECRET_KEY, algorithm='HS256')
	return token.decode()