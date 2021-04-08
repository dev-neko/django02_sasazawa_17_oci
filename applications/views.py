from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import SearchQueryModel
from config.tasks import add,search_url,search_seller
from celery.result import AsyncResult



def tame01_input(request):
	return render(request,'applications/tame01_input.html')

def tame01_output(request):
	if 'add_btn' in request.POST:
		x=int(request.POST['input_a'])
		y=int(request.POST["input_b"])
		celery_task=AsyncResult(add.delay(x,y).id)
	# elif 'reload_btn' in request.POST:
	else:
		celery_task=AsyncResult(request.POST['input_celery_task'])
	if celery_task.state=='SUCCESS':
		result_dt=celery_task.get()
		django_template_data={'result_dt':result_dt}
		return render(request,'applications/tame01_output.html',django_template_data)
	else:
		django_template_data={'celery_task':celery_task}
		return render(request,'applications/tame01_pending.html',django_template_data)


# def input_v1(request):
# 	if request.user.is_authenticated:
# 		# ここで初期化しないとリロードしても検索条件消えない
# 		dt_read_db_data=[]
# 		# フォームに入力する初期データ
# 		dt_exists_db_data={'exists_db_data':SearchQueryModel.objects.all()}
# 		# 検索条件保存ボタンか検索条件呼び出しボタンが押されたときの処理
# 		# これを付けないとリロードしたときにも保存処理が行われる
# 		if request.method=='POST':
# 			# ボタンを押したときnameでボタンを判定
# 			if request.POST["db_action_btn"]=="save":
# 				# idを指定しないと最後に追加される
# 				SearchQueryModel.objects.create(
# 					md_query_name=request.POST['query_name'],
# 					md_or_title=request.POST['or_title'],
# 					md_ex_title=request.POST['ex_title'],
# 					md_or_desc=request.POST['or_desc'],
# 					md_ex_desc=request.POST['ex_desc'],
# 					md_price_min=request.POST['price_min'],
# 					md_price_max=request.POST['price_max'],
# 				)
# 				# 登録後は最新のDBの内容を読み込んでDjangoテンプレートに渡す
# 				dt_read_db_data={'read_db_data':SearchQueryModel.objects.order_by("id").last()}
# 			elif request.POST["db_action_btn"]=="read":
# 				dt_read_db_data={'read_db_data':SearchQueryModel.objects.get(id=request.POST["select_db_data"])}
# 			elif request.POST["db_action_btn"]=="delete":
# 				SearchQueryModel.objects.filter(id=request.POST["select_db_data"]).delete()
# 			elif request.POST["db_action_btn"]=="all_delete":
# 				SearchQueryModel.objects.all().delete()
# 		dt_data={'dt_exists_db_data':dt_exists_db_data,
# 						 'dt_read_db_data':dt_read_db_data,
# 						 }
# 		return render(request, 'applications/input_v1.html', dt_data)
# 	else:
# 		return HttpResponseRedirect('/accounts/login/')

def output_v4(request):
	# print(request.POST)
	if "srch_submit_btn" in request.POST:
		# 何曜日の何時までに終了か取得
		if request.POST["radio_e_wday_e_time"]=="ON":
			e_wday_e_time="&e_wday="+request.POST["select_e_wday"]+"&e_time="+request.POST["select_e_time"]
		else:
			e_wday_e_time=""
		# 解析する範囲を取得
		if request.POST["radio_analysis_pages"]=='srch_end':
			post_analysis_pages_str='1'
			# ヤフオクでは最大150ページまでなのでforで回してNoneなら終了
			post_analysis_pages_end='150'
		elif request.POST["radio_analysis_pages"]=='srch_rng':
			post_analysis_pages_str=request.POST["analysis_pages_str"]
			post_analysis_pages_end=request.POST["analysis_pages_end"]
		# 追加のフィルタ
		post_rate=request.POST["rate"]
		post_exclude_id=request.POST["exclude_id"].split(',')
		post_exclude_titledesc=request.POST["exclude_titledesc"].split(' ')
		# タスクにするために追加で変数に入れた
		post_src_raw_url=request.POST["src_raw_url"]
		post_src_seller_url=request.POST["src_seller_url"]
		post_radio_ana_end_spec=request.POST["radio_ana_end_spec"]
		post_ana_end_spec=request.POST["ana_end_spec"]
		post_radio_auto_ext=request.POST["radio_auto_ext"]
		post_radio_rate=request.POST["radio_rate"]
		post_radio_exclude_id=request.POST["radio_exclude_id"]
		post_radio_exclude_titledesc=request.POST["radio_exclude_titledesc"]
		# 検索URLからデータ取得パターン
		if request.POST["radio_url"]=="search":
			celery_task=AsyncResult(search_url.delay(e_wday_e_time,post_analysis_pages_str,post_analysis_pages_end,post_rate,post_exclude_id,post_exclude_titledesc,post_src_raw_url,post_radio_ana_end_spec,post_ana_end_spec,post_radio_auto_ext,post_radio_rate,post_radio_exclude_id,post_radio_exclude_titledesc).id)
		# ストアURLからデータ取得パターン
		else:
			celery_task=AsyncResult(search_seller.delay(e_wday_e_time,post_analysis_pages_str,post_analysis_pages_end,post_rate,post_exclude_id,post_exclude_titledesc,post_src_seller_url,post_radio_ana_end_spec,post_ana_end_spec,post_radio_auto_ext,post_radio_rate,post_radio_exclude_id,post_radio_exclude_titledesc).id)
	else:
		celery_task=AsyncResult(request.POST['input_celery_task'])
	if celery_task.state=='SUCCESS':
		src_url_list,auc_data_dict=celery_task.get()
		# サブの1次元辞書データ
		auc_data_sub_dict={'検索URL':src_url_list}
		# Djangoテンプレートへ渡すデータ
		django_template_data={'auc_data':auc_data_dict,
													'sub_data':auc_data_sub_dict}
		return render(request,'applications/output_v4.html',django_template_data)
	else:
		django_template_data={'celery_task':celery_task}
		return render(request,'applications/pending.html',django_template_data)




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
				print(alert_sw_first_data)
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