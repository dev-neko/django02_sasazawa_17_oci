import time
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import bs4,requests,re
from django.shortcuts import render
from .models import SearchQueryModel
import sys

from django_celery_results.models import TaskResult
from config.tasks import add
from celery.result import AsyncResult



def ya_src_tool_v4(request):
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
		return render(request, 'applications/ya_src_tool_v4.html', dt_data)
	else:
		return HttpResponseRedirect('/accounts/login/')

def output_v4(request):
	print(request)
	# テンプレへ渡す辞書
	auc_data_dict=[]
	src_url_list=[]
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
	# 検索URLからデータ取得パターン
	if request.POST["radio_url"]=="search":
		'''
		追加 1
		'''
		for_flag=False
		for page_pos in range(int(post_analysis_pages_str),int(post_analysis_pages_end)+1):
			src_url=url_b_get_v2(request.POST["src_raw_url"],e_wday_e_time,page_pos)
			src_url_parser=requests.get(src_url)
			bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
			# 最後まで検索して商品が見つからなければbreak
			if '条件に一致する商品は見つかりませんでした。' in bs4obj.text:
				break
			# outputで表示するために検索URLをappend
			src_url_list.append(src_url)
			list_items_list=bs4obj.find_all("li",attrs={'class':'Product'})
			for list_items in list_items_list:
				'''
				追加 1
				'''
				# 画像URL
				auc_imgurl=list_items.find("img",attrs={'class':'Product__imageData'}).get('src')
				# オークション名
				auc_title=list_items.find("a",attrs={'class':'Product__titleLink'}).text
				# URL
				auc_url=list_items.find("a",attrs={'class':'Product__titleLink'}).get('href')
				# 出品者名
				auc_seller=list_items.find("a",attrs={'class':'Product__seller'}).text
				# 出品者のレート
				# 新規はレート無しなのでそれを考慮
				auc_rating=list_items.find("a",attrs={'class':'Product__rating'})
				if auc_rating:
					auc_rating=auc_rating.text
				else:
					auc_rating="0%"
				# 現在価格
				auc_price=list_items.find("span",attrs={'class':'Product__priceValue u-textRed'}).text.replace(",","").replace("1円開始","").replace("円","")
				# 即決価格
				if list_items.select('span[class="Product__priceValue"]'):
					auc_pricewin=list_items.select('span[class="Product__priceValue"]')[0].text.replace(",","").replace("1円開始","").replace("円","")
				else:
					auc_pricewin="-"
				# 入札数
				auc_bid=list_items.find("a",attrs={'class':'Product__bid'}).text
				'''
				追加 2
				'''
				# 「入札が0件になるページまで検索」が有効で入札が0件の場合はbreak
				# 1つ外側のforをbreakするためのフラグも変更
				if request.POST["radio_ana_end_spec"]=='ON' and request.POST["ana_end_spec"]=='入札が0件になるページまで検索' and auc_bid=='0':
					for_flag=True
					break
				# 「新着のNEWの印がなくなるページまで検索」が有効で「New!!」が無い場合はbreak
				# 1つ外側のforをbreakするためのフラグも変更
				if request.POST["radio_ana_end_spec"]=='ON' and request.POST["ana_end_spec"]=='新着のNEWの印がなくなるページまで検索' and list_items.find("span",attrs={'class':'Product__icon Product__icon--new'})==None:
					for_flag=True
					break
				'''
				追加 2
				'''
				# 残り時間(auc_time)は「残り日数か時間」と「終了日時」か「残り分」だけの組み合わせなので
				# 「終了日時」があれば「残り日数か時間」と「終了日時」を表示
				# 「終了日時」がなければ「残り分」だけ表示
				auc_time_dayhormin=list_items.find("span",attrs={'class':'Product__time'}).text
				auc_time_detail=list_items.find("span",attrs={'class':'u-textGray u-fontSize10'})
				if auc_time_detail:
					auc_time=auc_time_dayhormin+auc_time_detail.text
				else:
					auc_time=auc_time_dayhormin
				# オークションの詳細ページを解析
				auc_auto_ext,auc_desc,auc_title_desc=auc_detail_get(auc_url,auc_price,auc_pricewin,post_exclude_titledesc,auc_title)
				# ヤフオク標準検索機能以外の条件でスクレイピングしてフィルタ
				filter_judge=filter_judge_get(request,auc_auto_ext,post_rate,auc_rating,post_exclude_id,auc_seller,post_exclude_titledesc,auc_title_desc)
				# filter_judgeにNGが含まれていなければappendする
				if "NG" not in filter_judge:
					auc_data_dict.append({'画像URL':auc_imgurl,'オク名':auc_title,'オクURL':auc_url,'出品者ID':auc_seller,'評価レート':auc_rating,'現在価格':auc_price,'即決価格':auc_pricewin,'入札数':auc_bid,'残り時間':auc_time,'自動延長':auc_auto_ext,})
			'''
			追加 3
			'''
			if for_flag:
				break
			'''
			追加 3
			'''
	# ストアURLからデータ取得パターン
	else:
		'''
		追加 1
		'''
		for_flag=False
		for page_pos in range(int(post_analysis_pages_str),int(post_analysis_pages_end)+1):
			src_url=url_b_get_v2(request.POST["src_seller_url"],e_wday_e_time,page_pos)
			src_url_parser=requests.get(src_url)
			bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
			# 最後まで検索して商品が見つからなければbreak
			if '該当する商品はありません。' in bs4obj.text:
				break
			# outputで表示するために検索URLをappend
			src_url_list.append(src_url)
			'''
			追加 1
			'''
			# 出品者名
			# auc_seller=bs4obj.find("span",attrs={'class':'seller__name'}).text
			auc_seller=None
			# 出品者のレート
			auc_rating=None
			# ストアURLから検索する場合は0件だとなぜかエラー出るのでキャッチ
			try:
				list_items_list=bs4obj.find("div",attrs={'id':'list01'}).find_all("tr",attrs={'class':''})
				for list_items in list_items_list:
					if list_items.find("td",attrs={'class':'i'}):
						# 画像URL
						auc_imgurl=list_items.find("img",attrs={'':''}).get('src')
						# オークション名
						auc_title=list_items.find("h3",attrs={'':''}).find("a",attrs={'':''}).text
						# URL
						auc_url=list_items.find("h3",attrs={'':''}).find("a",attrs={'':''}).get('href')
						# 現在価格
						auc_price=list_items.find("td",attrs={'class':'pr1'}).text.replace(",","").replace("1円開始","").replace("円","").replace("\n","")
						# 即決価格
						auc_pricewin=list_items.find("td",attrs={'class':'pr2'}).text.replace(",","").replace("1円開始","").replace("円","").replace("\n","")
						# 入札数
						auc_bid=list_items.find("td",attrs={'class':'bi'}).text.replace("\n","")
						'''
						追加 2
						'''
						# 「入札が0件になるページまで検索」が有効で入札が0件の場合はbreak
						# 1つ外側のforをbreakするためのフラグも変更
						if request.POST["radio_ana_end_spec"]=='ON' and request.POST["ana_end_spec"]=='入札が0件になるページまで検索' and auc_bid=='－':
							for_flag=True
							break
						# 「新着のNEWの印がなくなるページまで検索」が有効で「New!!」が無い場合はbreak
						# 1つ外側のforをbreakするためのフラグも変更
						if request.POST["radio_ana_end_spec"]=='ON' and request.POST["ana_end_spec"]=='新着のNEWの印がなくなるページまで検索' and list_items.find("li",attrs={'class':'sic1'})==None:
							for_flag=True
							break
						'''
						追加 2
						'''
						# 残り時間 auc_time
						auc_time=list_items.find("td",attrs={'class':'ti'}).text.replace("\n","")
						# オークションの詳細ページを解析
						auc_auto_ext,auc_desc,auc_title_desc=auc_detail_get(auc_url,auc_price,auc_pricewin,post_exclude_titledesc,auc_title)
						# ヤフオク標準検索機能以外の条件でスクレイピングしてフィルタ
						filter_judge=filter_judge_get(request,auc_auto_ext,post_rate,auc_rating,post_exclude_id,auc_seller,post_exclude_titledesc,auc_title_desc)
						# filter_judgeにNGが含まれていなければappendする
						if "NG" not in filter_judge:
							auc_data_dict.append({'画像URL':auc_imgurl,'オク名':auc_title,'オクURL':auc_url,'出品者ID':auc_seller,'評価レート':auc_rating,'現在価格':auc_price,'即決価格':auc_pricewin,'入札数':auc_bid,'残り時間':auc_time,'自動延長':auc_auto_ext,})
				'''
				追加 3
				'''
				if for_flag:
					break
				'''
				追加 3
				'''
			except AttributeError:
				pass
	# サブの1次元辞書データ
	auc_data_sub_dict={'検索URL':src_url_list,}
	# Djangoテンプレートへ渡すデータ
	django_template_data={'auc_data':auc_data_dict,
												'sub_data':auc_data_sub_dict,
												}
	# print(django_template_data)
	return render(request, 'applications/output_v4.html', django_template_data)

def tame01_input(request):
	return render(request,'applications/tame01_input.html')

def tame01_output(request):
	if 'add_button' in request.POST:
		x=int(request.POST['input_a'])
		y=int(request.POST["input_b"])
		task_id=add.delay(x,y)
		result=AsyncResult(task_id.id)
		# result=add(x,y)
		# result=list(TaskResult.objects.all().values_list("result",flat=True))
		# if len(result)==0:
		# 	result[0]=0
		django_template_data={'result':result}
		return render(request,'applications/tame01_output.html',django_template_data)





"""関数"""
# オークションの詳細ページを解析
def auc_detail_get(auc_url,auc_price,auc_pricewin,post_exclude_titledesc,auc_title):
		# オークションの詳細ページを解析
		auc_url_parser=requests.get(auc_url)
		bs4obj_auc_url=bs4.BeautifulSoup(auc_url_parser.text,'html.parser')
		# 現在価格と即決価格が同じならば定額、異なればオークションと判断して
		# オークションの場合だけ自動延長の有無を確認
		# 自動延長の有無 auc_auto_ext
		if auc_price!=auc_pricewin:
			auc_auto_ext=bs4obj_auc_url.find("ul",attrs={'class':'ProductDetail__items ProductDetail__items--primary'}).find_all("dd",attrs={'class':'ProductDetail__description'})[
					3].text.replace("：","")
		else:
			auc_auto_ext="定額のオークション"
		# 商品説明 auc_desc
		# もしかしてエラー出るかも？
		# print(bs4obj_auc_url.find("div",attrs={'class':'ProductExplanation__commentBody js-disabledContextMenu'}))
		# print(auc_url)
		auc_desc=bs4obj_auc_url.find("div",attrs={'class':'ProductExplanation__commentBody js-disabledContextMenu'}).text
		# タイトルと商品説明で除外キーワードが部分一致しているか判定 auc_title_desc
		auc_title_desc="なし"
		for fo_post_exclude_titledesc in post_exclude_titledesc:
			if fo_post_exclude_titledesc in (auc_title+auc_desc):
				auc_title_desc="あり"
				break
		return auc_auto_ext, auc_desc, auc_title_desc
# ヤフオク標準検索機能以外の条件でスクレイピングしてフィルタ結果を返す
def filter_judge_get(request,auc_auto_ext,post_rate,auc_rating,post_exclude_id,auc_seller,post_exclude_titledesc,auc_title_desc):
	filter_judge=[]
	# 自動延長のフィルタ
	if request.POST["radio_auto_ext"]=="ON":
		if (auc_auto_ext=="なし"):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	# 評価レートフィルタ
	if request.POST["radio_rate"]=="ON" and post_rate!="":
		if float(auc_rating.replace("%",""))>float(post_rate):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	# 出品者IDフィルタ
	if request.POST["radio_exclude_id"]=="ON" and post_exclude_id[0]!="":
		if (auc_seller not in post_exclude_id):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	# タイトルと商品説明で部分一致除外フィルタ
	if request.POST["radio_exclude_titledesc"]=="ON" and post_exclude_titledesc[0]!="":
		if (auc_title_desc=="なし"):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	return filter_judge
# ヤフオクで絞り込んだURLの表示件数と解析ページ数から&b=を計算
# &b= も &n= もすでにURLに含まれているとする
def url_b_get(request,target_url,e_wday_e_time):
	# 1ページの表示数を取得
	post_dispn=re.search('[&?]n=([0-9]*)',target_url).groups()[0]
	# print(post_dispn)
	# &b= の数値を1ページの表示数と解析するページ数から計算する
	analysis_pages=1+int(post_dispn)*(int(request.POST["analysis_pages"])-1)
	# print(post_analysis_pages)
	# bs4で解析するURL
	# &b= で始まらない場合はエラーになるけど、そういうパターンはなさそうなのでとりあえずこれで
	src_url=re.sub('&b=[0-9]*',"&b="+str(analysis_pages),target_url)+e_wday_e_time
	print(src_url)
	return src_url
# ヤフオクで絞り込んだURLの表示件数と解析ページ数から&b=を計算
# &b= も &n= もすでにURLに含まれているとする
# forで回せるように改良
def url_b_get_v2(target_url,e_wday_e_time,page_pos):
	# 1ページの表示数を取得
	post_dispn=re.search('[&?]n=([0-9]*)',target_url).groups()[0]
	# print(post_dispn)
	# &b= の数値を1ページの表示数と解析するページ数から計算する
	analysis_pages=1+int(post_dispn)*(page_pos-1)
	# print(post_analysis_pages)
	# bs4で解析するURL
	# &b= で始まらない場合はエラーになるけど、そういうパターンはなさそうなのでとりあえずこれで
	src_url=re.sub('&b=[0-9]*',"&b="+str(analysis_pages),target_url)+e_wday_e_time
	# print(src_url)
	return src_url
"""関数"""