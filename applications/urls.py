from django.urls import path
from . import views

app_name='app_urls'

urlpatterns = [
	path('v1/',views.input_v1,name='input'),
	path('userdata/',views.userdata,name='userdata'),
	# path('tame01_input/',views.tame01_input),
	# path('tame01_input/tame01_output/',views.tame01_output),
]