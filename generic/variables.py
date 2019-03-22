LOGIN_URL = '/account/signin/'
FILE_CHUNK_SIZE = 2500000
PRODUCTS_FILE_PATH = 'data/product'
USER_THUMBNAIL_PATH = 'data/user'
SPACE_BANNER_PATH = 'data/space/banner'

REACT_GOOD_POINT = 4
REACT_BAD_POINT = -1
REACT_FAKE_POINT = -2
SPACE_FAVORITE_POINT = 5


ACTIVITY_POINT = {
	'GOOD' : 4,
	'BAD' : -2,
	'FAKE' : -1,
	'FAVORITE' : 5,
	'PIN' : 2
}

MAX_TRENDING_SPACE = 10
MIN_RATE_FOR_SPACE_TRENDING = 5

from time import time
def now_str(mul=1):
	"""
	current time in string format
	"""
	return str(int(time()*(10**mul)))


from uuid import uuid4
from hashlib import md5
def random():
	return str(md5(now_str(2).encode()+uuid4().hex.encode()).hexdigest())
