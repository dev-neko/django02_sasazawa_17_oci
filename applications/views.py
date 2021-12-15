from django.http import HttpResponseRedirect
from django.shortcuts import render

def input_v1(request):
	return render(request, 'applications/input_v1.html')