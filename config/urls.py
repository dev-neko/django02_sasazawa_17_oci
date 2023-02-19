from django.urls import include,path
from django.contrib import admin
from applications.views import frontpage


urlpatterns = [
	# トップページへのURLルーティングをapplicationsフォルダ内のurls.pyへ回す
	# path('',include('applications.urls')),

	path('', frontpage),

	# adminページの表示
	path('admin/', admin.site.urls,name='admin'),
	# ログイン関連ページの表示
	path('accounts/',include('django.contrib.auth.urls')),
]