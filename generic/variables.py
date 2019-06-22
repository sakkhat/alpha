from time import time
def now_string(mul=1):
	"""
	current time in string format
	"""
	return str(int(time()*(10**mul)))



from string import ascii_letters, digits
import random as _rand
def random_string(prefix='', size=12):
	symbols = '_-'
	return prefix.join(_rand.choices(ascii_letters+digits+symbols, k=size))


from api.handler.tokenization import encode
def get_api_token(request):
	token = request.session.get('user_api_token', None)
	if token is None:
		token = encode({'user_id':request.user.id})
		request.session['user_api_token'] = token
	return token