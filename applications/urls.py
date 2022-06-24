from django.urls import path
from . import views

app_name='app_urls'

urlpatterns = [
	path('',views.index,name='index'),
	path('dl_csv_zip/',views.dl_csv_zip,name='dl_csv_zip'),
	path('dl_csv_zip_proc/',views.dl_csv_zip_proc,name='dl_csv_zip_proc'),
]