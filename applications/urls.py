from django.urls import path
from . import views

# Djangoテンプレートで使用するためにURLルーティングの名前を付けておく
app_name='app_urls'

urlpatterns = [
	# トップページでは「applications/views.py」のindex関数を実行する
	path('',views.index,name='index'),

	# dl_csv_zip系
	# URL「~/dl_csv_zip/」にアクセスした際に「applications/views.py」のdl_csv_zip関数を実行させる
	path('dl_csv_zip/',views.dl_csv_zip,name='dl_csv_zip'),
	# URL「~/dl_csv_zip_proc/」にアクセスした際に「applications/views.py」のdl_csv_zip_proc関数を実行させる
	path('dl_csv_zip_proc/',views.dl_csv_zip_proc,name='dl_csv_zip_proc'),

	# rec_ajax系
	# URL「~/rec_ajax/」にアクセスした際に「applications/views.py」のrec_ajax関数を実行させる
	path('rec_ajax/',views.rec_ajax,name='rec_ajax'),
	# Ajax経由でURL「~/rec_ajax_proc/」にアクセスした際に「applications/views.py」のrec_ajax_proc関数を実行させる
	# 「name='rec_ajax_proc'」は後ほどrec_ajax.htmlで使用する
	path('rec_ajax_proc/',views.rec_ajax_proc,name='rec_ajax_proc'),

	# ヘルプボタン系
	# URL「~/help_modal/」にアクセスした際に「applications/views.py」のhelp_modal関数を実行させる
	path('help_modal/',views.help_modal,name='help_modal'),
]