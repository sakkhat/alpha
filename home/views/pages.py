from django.shortcuts import render, redirect, HttpResponse
from home.forms import FeedbackForm


def terms(request):
	return render(request, 'home/pages/terms.html', {})

def about(request):
	return render(request, 'home/pages/about.html', {})

def feedback(request):
	context = {}
	if request.method == 'POST':
		form = FeedbackForm(request.POST, user=request.user)
		if form.is_valid():
			form.save()
			context['sent'] = True

	form = FeedbackForm(user=request.user)
	context['form'] = form

	return render(request, 'home/pages/feedback.html', context)

def privacy_policy(request):
	return render(request, 'home/pages/privacy_policy.html', {})

def cookie(request):
	return render(request, 'home/pages/cookie.html', {})