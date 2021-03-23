from django.urls import include, path
from django.contrib import admin

urlpatterns = [
	path('admin/', admin.site.urls),
	path('work_apps/',include('applications.urls')),
	path('work_apps/accounts/',include('django.contrib.auth.urls')),
]