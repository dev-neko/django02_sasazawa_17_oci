from django.urls import path
from . import views

app_name='app_urls'

urlpatterns = [
	path('index/',views.index,name='index'),
]