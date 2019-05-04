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