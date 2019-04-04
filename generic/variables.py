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



DISTRICTS = (
	(0, 'Bagerhat'), 
	(1, 'Bandarban'), 
	(2, 'Barguna'), 
	(3, 'Barisal'), 
	(4, 'Bhola'), 
	(5, 'Bogra'), 
	(6, 'Brahmanbaria'), 
	(7, 'Chandpur'), 
	(8, 'Chapainawabganj'), 
	(9, 'Chittagong'), 
	(10, 'Chuadanga'), 
	(11, 'Comilla'), 
	(12, "Cox's Bazar"), 
	(13, 'Dhaka'), 
	(14, 'Dinajpur'), 
	(15, 'Faridpur'), 
	(16, 'Feni'), 
	(17, 'Gaibandha'), 
	(18, 'Gazipur'), 
	(19, 'Gopalganj'), 
	(20, 'Habiganj'), 
	(21, 'Jamalpur'), 
	(22, 'Jessore'), 
	(23, 'Jhalokati'), 
	(24, 'Jhenaidah'), 
	(25, 'Joypurhat'), 
	(26, 'Khagrachhari'), 
	(27, 'Khulna'), 
	(28, 'Kishoreganj'), 
	(29, 'Kurigram'), 
	(30, 'Kushtia'), 
	(31, 'Lakshmipur'), 
	(32, 'Lalmonirhat'), 
	(33, 'Madaripur'), 
	(34, 'Magura'), 
	(35, 'Manikganj'), 
	(36, 'Meherpur'), 
	(37, 'Moulvibazar'), 
	(38, 'Munshiganj'), 
	(39, 'Mymensingh'), 
	(40, 'Naogaon'), 
	(41, 'Narail'), 
	(42, 'Narayanganj'), 
	(43, 'Narsingdi'), 
	(44, 'Natore'), 
	(45, 'Netrakona'), 
	(46, 'Nilphamari'), 
	(47, 'Noakhali'), 
	(48, 'Pabna'), 
	(49, 'Panchagarh'), 
	(50, 'Patuakhali'), 
	(51, 'Pirojpur'), 
	(52, 'Rajbari'), 
	(53, 'Rajshahi'), 
	(54, 'Rangamati'), 
	(55, 'Rangpur'), 
	(56, 'Satkhira'), 
	(57, 'Shariatpur'), 
	(58, 'Sherpur'), 
	(59, 'Sirajganj'), 
	(60, 'Sunamganj'), 
	(61, 'Sylhet'), 
	(62, 'Tangail'), 
	(63, 'Thakurgaon')
)
