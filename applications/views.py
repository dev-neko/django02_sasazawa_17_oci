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


def input_v4(request):
	if request.user.is_authenticated:
		# ここで初期化しないとリロードしても検索条件消えない
		dt_read_db_data=[]
		# フォームに入力する初期データ
		dt_exists_db_data={'exists_db_data':SearchQueryModel.objects.all()}
		dt_wday_data={"0":"日曜日","1":"月曜日","2":"火曜日","3":"水曜日","4":"木曜日","5":"金曜日","6":"土曜日"}
		dt_time_data={str(x):str(x)+"時" for x in range(24)}
		dt_analysis_pages_data={str(x):str(x)+"ページ目" for x in range(1,31)}
		dt_ana_end_spec_data=['入札が0件になるページまで検索','新着のNEWの印がなくなるページまで検索']
		# 検索条件保存ボタンか検索条件呼び出しボタンが押されたときの処理
		# これを付けないとリロードしたときにも保存処理が行われる
		if request.method=='POST':
			# ボタンを押したときnameでボタンを判定
			if request.POST["db_action_btn"]=="save":
				# idを指定しないと最後に追加される
				SearchQueryModel.objects.create(
					md_query_name=request.POST["query_name"],
					md_radio_url=request.POST["radio_url"],
					md_src_url=request.POST["src_raw_url"],
					md_seller_url=request.POST["src_seller_url"],
					md_radio_e_wday_e_time=request.POST["radio_e_wday_e_time"],
					md_e_wday=request.POST["select_e_wday"],
					md_e_time=request.POST["select_e_time"],
					# md_analysis_pages=request.POST["analysis_pages"],
					md_analysis_pages_radio=request.POST["radio_analysis_pages"],
					md_analysis_pages_str=request.POST["analysis_pages_str"],
					md_analysis_pages_end=request.POST["analysis_pages_end"],
					md_radio_ana_end_spec=request.POST["radio_ana_end_spec"],
					md_ana_end_spec=request.POST["ana_end_spec"],
					md_auto_ext=request.POST["radio_auto_ext"],
					md_rate_radio=request.POST["radio_rate"],
					md_rate=request.POST["rate"],
					md_exclude_id_radio=request.POST["radio_exclude_id"],
					md_exclude_id=request.POST["exclude_id"],
					md_exclude_titledesc_radio=request.POST["radio_exclude_titledesc"],
					md_exclude_titledesc=request.POST["exclude_titledesc"],
				)
				# 登録後は最新のDBの内容を読み込んでDjangoテンプレートに渡す
				dt_read_db_data={'read_db_data':SearchQueryModel.objects.order_by("id").last()}
			elif request.POST["db_action_btn"]=="read":
				dt_read_db_data={'read_db_data':SearchQueryModel.objects.get(id=request.POST["select_db_data"])}
			elif request.POST["db_action_btn"]=="delete":
				SearchQueryModel.objects.filter(id=request.POST["select_db_data"]).delete()
			elif request.POST["db_action_btn"]=="all_delete":
				SearchQueryModel.objects.all().delete()
		dt_data={'dt_exists_db_data':dt_exists_db_data,
						 'dt_read_db_data':dt_read_db_data,
						 'dt_wday_data':dt_wday_data,
						 'dt_time_data':dt_time_data,
						 'dt_analysis_pages_data':dt_analysis_pages_data,
						 'dt_ana_end_spec_data':dt_ana_end_spec_data,
						 }
		return render(request, 'applications/input_v4.html', dt_data)
	else:
		return HttpResponseRedirect('/accounts/login/')

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