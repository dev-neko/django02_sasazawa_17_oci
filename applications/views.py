from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import SearchQueryModel,UserDataModel
from config.tasks import add,search_url,search_seller
from celery.result import AsyncResult



def input_v1(request):
	if request.user.is_authenticated:
		# ここで初期化しないとリロードしても検索条件消えない
		read_db=[]
		# DBに保存されている全ての内容を取得
		exists_db=SearchQueryModel.objects.all()
		# 検索条件保存ボタンか検索条件呼び出しボタンが押されたときの処理
		# これを付けないとリロードしたときにも保存処理が行われる
		if request.method=='POST':
			# ボタンを押したときnameでボタンを判定
			if request.POST["db_action_btn"]=="save":
				# チェックボックスの内容をリストにすると空でもエラー出ない
				if len(request.POST.getlist('alert_sw_first')):
					alert_sw_first_data='checked'
				else:
					alert_sw_first_data='nocheck'
				# idを指定しないと最後に追加される
				SearchQueryModel.objects.create(
					md_query_name=request.POST['query_name'],
					md_or_title=request.POST['or_title'],
					md_ex_title=request.POST['ex_title'],
					md_or_desc=request.POST['or_desc'],
					md_ex_desc=request.POST['ex_desc'],
					md_price_min=request.POST['price_min'],
					md_price_max=request.POST['price_max'],
					md_alert_sw=alert_sw_first_data,
				)
				# print(alert_sw_first_data)
				# 登録後は最新のDBの内容を読み込んでDjangoテンプレートに渡す
				read_db=SearchQueryModel.objects.order_by("id").last()
			elif request.POST["db_action_btn"]=="read":
				read_db=SearchQueryModel.objects.get(id=request.POST["select_db_data"])
			elif request.POST["db_action_btn"]=="delete":
				SearchQueryModel.objects.filter(id=request.POST["select_db_data"]).delete()
			elif request.POST["db_action_btn"]=="all_delete":
				SearchQueryModel.objects.all().delete()
			# alert_sw の更新、exists_db 更新してないのに何でボタンクリックしたら変更反映されてる？
			elif request.POST["db_action_btn"]=="alert_sw":
				for sqm_obj in SearchQueryModel.objects.all():
					tmp_db=SearchQueryModel.objects.get(id=sqm_obj.id)
					if str(sqm_obj.id) in request.POST.getlist('alert_sw_all'):
						tmp_db.md_alert_sw='checked'
					else:
						tmp_db.md_alert_sw='nocheck'
					tmp_db.save()
		dt_data={'exists_db':exists_db,
						 'read_db':read_db,
						 }
		return render(request, 'applications/input_v1.html', dt_data)
	else:
		return HttpResponseRedirect('/accounts/login/')

def userdata(request):
	if request.user.is_authenticated:
		exists_db=UserDataModel.objects.all()
		if request.method=='POST':
			UserDataModel.objects.update_or_create(md_name='user data',
																						 defaults={'md_line_token':request.POST['line_token']})
		dt_data={'exists_db':exists_db}
		return render(request, 'registration/userdata.html',dt_data)
	else:
		return HttpResponseRedirect('/accounts/login/')