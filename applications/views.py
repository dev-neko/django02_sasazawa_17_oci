from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
	# ログインの確認
	if request.user.is_authenticated:
		return render(request,'applications/index.html')
	else:
		return HttpResponseRedirect('/accounts/login/')