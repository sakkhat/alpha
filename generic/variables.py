LOGIN_URL = '/account/signin/'
FILE_CHUNK_SIZE = 2500000
PRODUCTS_FILE_PATH = 'data/product'
USER_THUMBNAIL_PATH = 'data/user'
SPACE_BANNER_PATH = 'data/space/banner'

REACT_GOOD_POINT = 3
REACT_BAD_POINT = -1
REACT_FAKE_POINT = -2
PRODUCT_PIN = 2
SPACE_FAVORITE_POINT = 4


ACTIVITY_POINT = {
	'GOOD' : 4,
	'BAD' : -1,
	'FAKE' : -2,
	'FAVORITE' : 5,
	'PIN' : 2
}

MAX_TRENDING_SPACE = 10
MAX_TRENDING_PRODUCT = 8
MIN_RATE_FOR_SPACE_TRENDING = 5
PRODUCT_PAGINATION_SIZE = 4
SPACE_PAGINATION_SIZE = 4

BASE_POST_FEE = 22


from time import time
def now_str(mul=1):
	"""
	current time in string format
	"""
	return str(int(time()*(10**mul)))

