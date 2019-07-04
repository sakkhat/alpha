from api.handler.tokenization import encode
from base64 import encodestring as __encode_string
from base64 import decodestring as __decode_string
import random as _rand
from hashlib import sha256
from string import ascii_letters, digits
from uuid import UUID


def is_valid_uuid(uuid):
	try:
		return UUID(uuid)
	except ValueError as e:
		return None


def random_string(prefix='', size=12):
	symbols = '_-'
	return prefix.join(_rand.choices(ascii_letters+digits+symbols, k=size))


def get_api_token(request):
	token = request.session.get('user_api_token', None)
	if token is None:
		token = encode({'user_id':request.user.id})
		request.session['user_api_token'] = token
	return token


def hashing_into_int(string, length=24):
	string = string.lower()
	return int(sha256(string.encode()).hexdigest(), 16) % 10**length