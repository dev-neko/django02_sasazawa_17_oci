from django.urls import path
from . import views

urlpatterns = [
	path('v4/',views.ya_src_tool_v4),
	path('v4/output/',views.output_v4),
]