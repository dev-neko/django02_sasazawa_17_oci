from django.urls import path
from . import views

urlpatterns = [
	path('v1/',views.input_v1),
	# path('v4/output/',views.output_v4),
	# path('tame01_input/',views.tame01_input),
	# path('tame01_input/tame01_output/',views.tame01_output),
]