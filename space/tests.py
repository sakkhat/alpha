

def foo(name, **kwargs):
	print(name)

	print(kwargs)
	print(kwargs.pop('schoo', None))





foo('Rafi', schoo='RS', college='CVC', university='SUST')