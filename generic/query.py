from home.models import PinnedProduct

from space.models import Product


def pinned_product_objects(user, limit=-1):
	if limit <= 0:
		query_uid = PinnedProduct.objects.filter(user=user).values('product_id').order_by('-uid')
	else:
		query_uid = PinnedProduct.objects.filter(user=user).values('product_id').order_by('-uid')[:limit]
	uid_list = []
	for item in list(query_uid):
		uid_list.append(item['product_id'])
	pinned_products = Product.objects.filter(uid__in=uid_list).order_by('-uid')

	return pinned_products