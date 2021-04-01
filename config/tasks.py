from __future__ import absolute_import, unicode_literals
import re,bs4,requests
from celery import shared_task
import time



@shared_task
def add(x,y):
	print("処理中")
	z = x + y
	time.sleep(10)
	print("処理完了")
	return z

@shared_task
def search_url(e_wday_e_time,
							 post_analysis_pages_str,
							 post_analysis_pages_end,
							 post_rate,
							 post_exclude_id,
							 post_exclude_titledesc,
							 post_src_raw_url,
							 post_radio_ana_end_spec,
							 post_ana_end_spec,
							 post_radio_auto_ext,
							 post_radio_rate,
							 post_radio_exclude_id,
							 post_radio_exclude_titledesc):
	# テンプレへ渡す辞書
	auc_data_dict=[]
	src_url_list=[]
	for_flag=False
	for page_pos in range(int(post_analysis_pages_str),int(post_analysis_pages_end)+1):
		src_url=url_b_get_v2(post_src_raw_url,e_wday_e_time,page_pos)
		src_url_parser=requests.get(src_url)
		bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# 最後まで検索して商品が見つからなければbreak
		if '条件に一致する商品は見つかりませんでした。' in bs4obj.text:
			break
		# outputで表示するために検索URLをappend
		src_url_list.append(src_url)
		list_items_list=bs4obj.find_all("li",attrs={'class':'Product'})
		for list_items in list_items_list:
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
			# 「入札が0件になるページまで検索」が有効で入札が0件の場合はbreak
			# 1つ外側のforをbreakするためのフラグも変更
			if post_radio_ana_end_spec=='ON' and post_ana_end_spec=='入札が0件になるページまで検索' and auc_bid=='0':
				for_flag=True
				break
			# 「新着のNEWの印がなくなるページまで検索」が有効で「New!!」が無い場合はbreak
			# 1つ外側のforをbreakするためのフラグも変更
			if post_radio_ana_end_spec=='ON' and post_ana_end_spec=='新着のNEWの印がなくなるページまで検索' and list_items.find("span",attrs={'class':'Product__icon Product__icon--new'})==None:
				for_flag=True
				break
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
			filter_judge=filter_judge_get_v2(post_radio_auto_ext,
																			 post_radio_rate,
																			 post_radio_exclude_id,
																			 post_radio_exclude_titledesc,
																			 auc_auto_ext,
																			 post_rate,
																			 auc_rating,
																			 post_exclude_id,
																			 auc_seller,
																			 post_exclude_titledesc,
																			 auc_title_desc)
			# filter_judgeにNGが含まれていなければappendする
			if "NG" not in filter_judge:
				auc_data_dict.append({'画像URL':auc_imgurl,'オク名':auc_title,'オクURL':auc_url,'出品者ID':auc_seller,'評価レート':auc_rating,'現在価格':auc_price,'即決価格':auc_pricewin,'入札数':auc_bid,'残り時間':auc_time,'自動延長':auc_auto_ext,})
		if for_flag:
			break
	return src_url_list,auc_data_dict

@shared_task
def search_seller(e_wday_e_time,
									post_analysis_pages_str,
									post_analysis_pages_end,
									post_rate,
									post_exclude_id,
									post_exclude_titledesc,
									post_src_seller_url,
									post_radio_ana_end_spec,
									post_ana_end_spec,
									post_radio_auto_ext,
									post_radio_rate,
									post_radio_exclude_id,
									post_radio_exclude_titledesc):
	# テンプレへ渡す辞書
	auc_data_dict=[]
	src_url_list=[]
	for_flag=False
	for page_pos in range(int(post_analysis_pages_str),int(post_analysis_pages_end)+1):
		src_url=url_b_get_v2(post_src_seller_url,e_wday_e_time,page_pos)
		src_url_parser=requests.get(src_url)
		bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# 最後まで検索して商品が見つからなければbreak
		if '該当する商品はありません。' in bs4obj.text:
			break
		# outputで表示するために検索URLをappend
		src_url_list.append(src_url)
		# 出品者名
		# auc_seller=bs4obj.find("span",attrs={'class':'seller__name'}).text
		auc_seller=None
		# 出品者のレート
		auc_rating=None
		# ストアURLから検索する場合は0件だとなぜかエラー出るのでキャッチ→0件の場合はbreakするので削除
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
				# 「入札が0件になるページまで検索」が有効で入札が0件の場合はbreak
				# 1つ外側のforをbreakするためのフラグも変更
				if post_radio_ana_end_spec=='ON' and post_ana_end_spec=='入札が0件になるページまで検索' and auc_bid=='－':
					for_flag=True
					break
				# 「新着のNEWの印がなくなるページまで検索」が有効で「New!!」が無い場合はbreak
				# 1つ外側のforをbreakするためのフラグも変更
				if post_radio_ana_end_spec=='ON' and post_ana_end_spec=='新着のNEWの印がなくなるページまで検索' and list_items.find("li",attrs={'class':'sic1'})==None:
					for_flag=True
					break
				# 残り時間 auc_time
				auc_time=list_items.find("td",attrs={'class':'ti'}).text.replace("\n","")
				# オークションの詳細ページを解析
				auc_auto_ext,auc_desc,auc_title_desc=auc_detail_get(auc_url,auc_price,auc_pricewin,post_exclude_titledesc,auc_title)
				# ヤフオク標準検索機能以外の条件でスクレイピングしてフィルタ
				filter_judge=filter_judge_get_v2(post_radio_auto_ext,
																				 post_radio_rate,
																				 post_radio_exclude_id,
																				 post_radio_exclude_titledesc,
																				 auc_auto_ext,
																				 post_rate,
																				 auc_rating,
																				 post_exclude_id,
																				 auc_seller,
																				 post_exclude_titledesc,
																				 auc_title_desc)
				# filter_judgeにNGが含まれていなければappendする
				if "NG" not in filter_judge:
					auc_data_dict.append(
						{'画像URL':auc_imgurl,'オク名':auc_title,'オクURL':auc_url,'出品者ID':auc_seller,'評価レート':auc_rating,
						 '現在価格':auc_price,'即決価格':auc_pricewin,'入札数':auc_bid,'残り時間':auc_time,'自動延長':auc_auto_ext,})
		if for_flag:
			break
	return src_url_list,auc_data_dict



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
			auc_auto_ext=bs4obj_auc_url.find("ul",attrs={'class':'ProductDetail__items ProductDetail__items--primary'}).find_all("dd",attrs={'class':'ProductDetail__description'})[3].text.replace("：","")
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
def filter_judge_get_v2(post_radio_auto_ext,
												post_radio_rate,
												post_radio_exclude_id,
												post_radio_exclude_titledesc,
												auc_auto_ext,
												post_rate,
												auc_rating,
												post_exclude_id,
												auc_seller,
												post_exclude_titledesc,
												auc_title_desc):
	filter_judge=[]
	# 自動延長のフィルタ
	if post_radio_auto_ext=="ON":
		if (auc_auto_ext=="なし"):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	# 評価レートフィルタ
	if post_radio_rate=="ON" and post_rate!="":
		if float(auc_rating.replace("%",""))>float(post_rate):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	# 出品者IDフィルタ
	if post_radio_exclude_id=="ON" and post_exclude_id[0]!="":
		if (auc_seller not in post_exclude_id):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	# タイトルと商品説明で部分一致除外フィルタ
	if post_radio_exclude_titledesc=="ON" and post_exclude_titledesc[0]!="":
		if (auc_title_desc=="なし"):
			filter_judge.append("OK")
		else:
			filter_judge.append("NG")
	else:
		filter_judge.append("OK")
	return filter_judge
# ヤフオクで絞り込んだURLの表示件数と解析ページ数から&b=を計算
# &b= も &n= もすでにURLに含まれているとする
# forで回せるように改良
def url_b_get_v2(target_url,e_wday_e_time,page_pos):
	# 1ページの表示数を取得
	post_dispn=re.search('[&?]n=([0-9]*)',target_url).groups()[0]
	# &b= の数値を1ページの表示数と解析するページ数から計算する
	analysis_pages=1+int(post_dispn)*(page_pos-1)
	# bs4で解析するURL
	# &b= で始まらない場合はエラーになるけど、そういうパターンはなさそうなのでとりあえずこれで
	src_url=re.sub('&b=[0-9]*',"&b="+str(analysis_pages),target_url)+e_wday_e_time
	return src_url
"""関数"""