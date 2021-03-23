from django.urls import path
from . import views

urlpatterns = [
	# path('ya_src_tool/dev/',views.dev_input),
	# path('ya_src_tool/dev/output',views.dev_output),
	path('ya_src_tool/',views.ya_src_tool),
	path('ya_src_tool/output', views.output),
	path('ya_src_tool_v2/',views.ya_src_tool_v2),
	path('ya_src_tool_v2/output_v2',views.output_v2),
	path('ya_src_tool/v3/',views.ya_src_tool_v3),
	path('ya_src_tool/v3/output',views.output_v3),
]