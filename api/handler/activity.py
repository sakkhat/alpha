from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min

from home.models import Favorite, PinnedProduct

from generic.variables import (ACTIVITY_POINT,MAX_TRENDING_SPACE,
	MIN_RATE_FOR_SPACE_TRENDING)

from space.models import Product, ProductReact, Space, Status


def handle_pin(user, uid, req):
	req = req.strip()
	req = req.upper()
	if req =='ADD' or req == 'REMOVE':
		try:
			product = Product.objects.get(uid = uid)
			space = Space.objects.get(id=product.space_id)
			if space.owner_id == user.id:
				return False
			status = Status.objects.get(space_id = product.space_id)

			if req == 'ADD':
				try:
					pin = PinnedProduct.objects.get(user_id=user.id, product_id=product.uid)
					return False
				except ObjectDoesNotExist as e:
					pin = PinnedProduct(user_id=user.id, product_id=product.uid)
					pin.save()

					status.total_pinned += 1
					status.rating = _addition(status.rating, ACTIVITY_POINT['PIN'])
					status.save()

					return True
			else:
				try:
					pin = PinnedProduct.objects.get(user_id=user.id, product_id=product.uid)
					pin.delete()

					status.total_pinned -= 1
					status.rating = _addition(status.rating, -ACTIVITY_POINT['PIN'])
					status.save()

					return True

				except ObjectDoesNotExist as e:
					pass

		except ObjectDoesNotExist as e:
			pass
	return False


def handle_react(user, uid, what):
	_REACTS = ['GOOD', 'BAD', 'FAKE', 'NONE']

	what = what.strip()
	what = what.upper()

	if  what in _REACTS:
		try:
			product = Product.objects.get(uid=uid)
			space = Space.objects.get(id=product.space_id)
			if space.owner_id == user.id:
				return None

			status = Status.objects.get(space_id=product.space_id)

			react_obj = None

			try:
				react_obj = ProductReact.objects.get(product_id=product.uid, user_id=user.id)
			except ObjectDoesNotExist as e:
				react_obj = None

			if react_obj is None:
				if what != 'NONE':
					if what == 'GOOD':
						_increase_good_react(product, status)
						new_react_obj = ProductReact(user_id=user.id, product_id=product.uid, react='G')
						
					elif what == 'BAD':
						_increase_bad_react(product, status)
						new_react_obj = ProductReact(user_id=user.id, product_id=product.uid, react='B')

					elif what == 'FAKE':
						_increase_fake_react(product, status)
						new_react_obj = ProductReact(user_id=user.id, product_id=product.uid, react='F')

					new_react_obj.save()

			else:
				_decrease_current_react(react_obj, product, status)
				if what != 'NONE':
					if what == 'GOOD':
						_increase_good_react(product, status)
						react_obj.react = 'G'
					elif what == 'BAD':
						_increase_bad_react(product, status)
						react_obj.react = 'B'

					elif what == 'FAKE':
						_increase_fake_react(product, status)
						react_obj.react = 'F'

					react_obj.save()

				else:
					react_obj.delete()

			product.save()
			status.save()

			return product

		except ObjectDoesNotExist as e:
			pass
	return None


def handle_favorite(user, name, req):

	if not user.is_authenticated:
		return False
	try:
		space = Space.objects.get(name__iexact=name)
		if space.owner_id == user.id:
			return False			
		
		req = req.strip()
		req = req.upper()

		if req == 'ADD' or req == 'REMOVE':
			try:
				row = Favorite.objects.get(user_id=user.id, space_id=space.id)
			except ObjectDoesNotExist as e:
				row = None

			status = Status.objects.get(space_id=space.id)

			if req == 'ADD':
				if row is None:
					row = Favorite(user_id=user.id, space_id=space.id)
					row.save()

					status.total_favorite += 1
					status.rating = _addition(status.rating, ACTIVITY_POINT['FAVORITE'])
					status.save()

					return True
				
			else:
				if row is not None:
					row.delete()

					status.total_favorite -= 1
					status.rating = _addition(status.rating, -ACTIVITY_POINT['FAVORITE'])
					status.save()
					
					return True

	except ObjectDoesNotExist as e:
		pass
	return False


def _decrease_current_react(react_obj, product, status):
	if react_obj.react == 'G':
		_decrease_good_react(product, status)

	elif react_obj.react == 'B':
		_decrease_bad_react(product, status)

	else:
		_decrease_fake_react(product, status)

def _addition(value1, value2):
	if value1 + value2 >= 0:
		return value1 + value2
	return value1

def _increase_good_react(product, status):
	product.react_good += 1
	status.total_good_react += 1
	status.rating = _addition(status.rating, ACTIVITY_POINT['GOOD'])

def _increase_bad_react(product, status):
	product.react_bad += 1
	status.total_bad_react += 1
	status.rating = _addition(status.rating, ACTIVITY_POINT['BAD'])

def _increase_fake_react(product, status):
	product.react_fake += 1
	status.total_fake_react += 1
	status.rating = _addition(status.rating, ACTIVITY_POINT['FAKE'])

def _decrease_good_react(product, status):
	product.react_good -= 1
	status.total_good_react -= 1
	status.rating = _addition(status.rating, -ACTIVITY_POINT['GOOD'])

def _decrease_bad_react(product, status):
	product.react_bad -= 1
	status.total_bad_react -= 1
	status.rating = _addition(status.rating, ACTIVITY_POINT['BAD'])

def _decrease_fake_react(product, status):
	product.react_fake -= 1
	status.total_fake_react -= 1
	status.rating = _addition(status.rating, ACTIVITY_POINT['FAKE'])

