from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse

from account.forms import PasswordChangeForm
from account.models import Account

from generic.variables import LOGIN_URL


def manager(request):
	what = request.GET.get('what', None)
	if what is None:
		pass
	elif len(what) is 0:
		pass
	else:
		what = what.lower()
		print(what)
		print(what == 'change')
		if what == 'reset':
			return reset(request)
		elif what == 'forget':
			return forget(request)
		elif what == 'change':
			return change(request)

	return HttpResponse('invalid')


def reset(request):
	return HttpResponse('Password Reset')


def forget(request):
	return HttpResponse('Password Forget')

#@login_required(login_url=LOGIN_URL)
def change(request):
	context = {}

	if request.method == 'POST':
		form = PasswordChangeForm(request.POST)
		if form.is_valid():
			confirm_password = form.cleaned_data['confirm_password']
			request.user.set_password(confirm_password)
			request.user.save()

	else:
		form = PasswordChangeForm()

	context['form'] = form

	return render(request, 'account/password/change.html', context)