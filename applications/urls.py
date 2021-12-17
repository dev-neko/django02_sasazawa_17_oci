from django.urls import path
from . import views

app_name='app_urls'

urlpatterns = [
	path('v1/',views.input_v1,name='input'),
	path('ajax_proc/',views.ajax_proc,name='ajax_proc'),  #-(3)
]