LOGIN_URL = '/account/signin/'
FILE_CHUNK_SIZE = 2500000
PRODUCTS_FILE_PATH = 'data/product'


from time import time
def now_str(mul=1):
	"""
	current time in string format
	"""
	return str(int(time()*(10**mul)))

from hashlib import md5
def now_md5_hashed(mul=1):
	t = now_str(mul)
	return md5(t.encode()).hexdigest()