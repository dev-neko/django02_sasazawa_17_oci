from django.urls import path
from . import views

urlpatterns = [
	path('v4/',views.input_v4),
	path('v4/output/',views.output_v4),
	# path('tame01_input/',views.tame01_input),
	# path('tame01_input/tame01_output/',views.tame01_output),
]