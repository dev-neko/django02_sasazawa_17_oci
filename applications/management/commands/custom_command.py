import pprint
import re
import sys
import time
# import winsound
from datetime import datetime
from selenium import webdriver
from applications.models import SearchQueryModel,UserDataModel
from django.core.management.base import BaseCommand, CommandError
import bs4,requests

# ------------------------------
# キタムラ
# ------------------------------
# 「カテゴリ指定なし、更新日順、100件表示」でURLのリストを取得
def get_url_list_kitamura():
	items_url_list=[]
	add_url='https://www.net-chuko.com'
	src_url='https://www.net-chuko.com/buy/list.do?keyword=&ob=ud-&lc=100&pg=1'
	src_url_parser=requests.get(src_url)
	bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
	items_list=bs4obj.find_all("li",attrs={'class':'item-element'})
	for items in items_list:
		# 商品URL
		items_url=items.find("a",attrs={'class':'item-photo'}).get('href')
		items_url_list.append(add_url+re.sub(r'&pp=a1-2','',items_url))
	# print(len(items_url_list))
	# print(items_url_list)
	return items_url_list
# 商品URLから必要な情報を取得
def get_detail_kitamura(update_url_list,self):
	add_url='https://www.net-chuko.com'
	items_detail_dict=[]
	while True:
		for f_count,update_url in enumerate(update_url_list):
			src_url_parser=requests.get(update_url)
			bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
			# タイトル
			items_title=bs4obj.find("h1").text
			if items_title=='該当する商品データがありません': continue
			# エラーが発生した場合は break して else を飛ばして while に戻りもう一度同じところから for を実行させる
			if items_title=='システムエラーが発生いたしました':
				self.stdout.write(str(f'もともとのURL\n{update_url_list}\n\n'))
				update_url_list=update_url_list[f_count:len(update_url_list)]
				self.stdout.write(str(f'エラーが発生したURL\n{update_url}\n\n'))
				self.stdout.write(str(f'残りのURL\n{update_url_list}\n\n'))
				break
			# 価格
			try:
				items_price=bs4obj.find("p",attrs={'class':'price'}).text
			except AttributeError:
				self.stdout.write(str(f'priceのエラーが表示されたので次のtryへ\n\n'))
				try:
					items_price=bs4obj.find("span",attrs={'class':'font-large text-red'}).text+' (税込)'
					# self.stdout.write(str(f'次のtryで取得したprice：\n{items_price}\n\n'))
					# sys.exit()
				except AttributeError:
					self.stdout.write(str(f'priceのエラーが表示されたURL；\n{update_url}\n\n'))
					self.stdout.write(str(f'priceのエラーが表示されたソース：\n{bs4obj}\n\n'))
					sys.exit()
			# 画像URL
			items_imgurl=add_url+bs4obj.find("p",attrs={'class':'img'}).find("img").get('src')
			# 商品説明文
			th_list=bs4obj.find_all("th",attrs={'class':'contents'})
			items_desc=''
			for elem in th_list:
				if '備考' in str(elem.string) or '付属品' in str(elem.string):
					items_desc+=elem.parent.find('td').text
			items_detail_dict.append({'タイトル':items_title,
																'価格':items_price,
																'画像URL':items_imgurl,
																'商品説明文':items_desc,
																'商品URL':update_url,
																})
		else:
			break
	return items_detail_dict
# キタムラの商品一覧ページから必要な情報を取得
# サイトがリニューアルされて一覧に詳細も表示されるように変更された
def get_detail_kitamura_selenium(driver):
	items_detail_dict=[]
	add_url='https://shop.kitamura.jp'
	src_url="https://shop.kitamura.jp/ec/list?type=u&sort=update_date&limit=100"
	driver.get(src_url)
	bs4obj=bs4.BeautifulSoup(driver.page_source,'html.parser')
	items_list=bs4obj.select('div[class="product-area"]')
	# print(items_list)
	for items in items_list:
		# 商品URL
		items_url=add_url+items.select_one('a[class="product-link"]').get('href')
		# タイトル
		items_title=items.select_one('div[class="product-name"]').text
		# 価格
		items_price=items.select_one('span[class="product-price"]').text
		# 画像URL
		items_imgurl=items.select_one('img[class="product-img"]').get('src')
		# 商品説明文
		items_desc=items.select_one('span[class="product-note-val"]').text
		items_detail_dict.append({'タイトル':items_title,
															'価格':items_price,
															'画像URL':items_imgurl,
															'商品説明文':items_desc,
															'商品URL':items_url,
															})
	# pprint.pprint(items_detail_dict)
	return items_detail_dict
# キタムラの新旧の商品詳細辞書を比較する
def compare_detail_dict_kitamura(old_detail_dict_kitamura,new_detail_dict_kitamura):
	update_detail_dict=[]
	for i in new_detail_dict_kitamura[:50]:
		for j in old_detail_dict_kitamura:
			if i['商品URL'] in j.values():
				break
		else:
			update_detail_dict.append(i)
	return update_detail_dict

# ------------------------------
# ネットモール
# ------------------------------
# 「カメラカテゴリ、更新日順、90件表示」でURLのリストを取得
def get_url_list_netmall():
	items_url_list=[]
	src_url='https://netmall.hardoff.co.jp/cate/00010003/?p=1&s=1&pl=90'
	src_url_parser=requests.get(src_url)
	bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
	items_list=bs4obj.find_all("a",attrs={'class':'p-goods__link'})
	for items in items_list:
		# 商品URL
		items_url_list.append(items.get('href'))
	# print(len(items_url_list))
	# print(items_url_list)
	return items_url_list
# 商品URLから必要な情報を取得
def get_detail_netmall(update_url_list):
	items_detail_dict=[]
	add_url='https://netmall.hardoff.co.jp'
	for update_url in update_url_list:
		src_url_parser=requests.get(update_url)
		bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# タイトル
		try:
			items_title=bs4obj.find("h2",attrs={'class':'p-goodsDetail__name'}).text
		except AttributeError:
			# カテゴリと商品名が同じ場合は商品名が省略されてカテゴリだけになる
			items_title=bs4obj.find("p",attrs={'class':'p-goodsDetail__category'}).text
		# 価格
		items_price=bs4obj.find("p",attrs={'class':'p-goodsDetail__price'}).text.replace('\n','')
		# 画像URL
		items_imgurl=bs4obj.find("img",attrs={'class':'p-goodsDetail__mainImg js-lightbox js-object-fit'}).get('src')
		if items_imgurl=='/images/goods/blankimg_itemphoto_noimage.png':
			items_imgurl=add_url+items_imgurl
		# 商品説明文
		tr_list=bs4obj.find("div",attrs={'class':'p-goodsGuide__body'}).find_all("tr")
		items_desc=''
		for elem in tr_list:
			if '付属レンズ'==elem.find('th').text or '特徴・備考'==elem.find('th').text:
				items_desc+=elem.find('td').text
		items_detail_dict.append({'タイトル':items_title.replace('　',' '),
															'価格':items_price,
															'画像URL':items_imgurl,
															'商品説明文':items_desc.replace('　',' '),
															'商品URL':update_url,
															})
	# print(items_detail_dict)
	# print(items_detail_dict[2]['商品説明文'])
	return items_detail_dict

# ------------------------------
# LINE notify
# ------------------------------
# LINEで通知を送信する、画像サムネイル表示も可能
def send_line_notify(token,message,image):
	line_notify_api = 'https://notify-api.line.me/api/notify'
	headers = {'Authorization': f'Bearer {token}'}
	data = {'message': message,
					'imageFullsize':image,
					'imageThumbnail':image}
	requests.post(line_notify_api, headers=headers, data=data)
# LINEトークンをDBから取得
for item in UserDataModel.objects.all():
	line_notify_token=item.md_line_token
# 辞書の内容を整形して通知
def send_alert_content(alert_content_dict):
	pipe='------------------------------'
	send_line_notify(line_notify_token,pipe,'')
	for alert_content in alert_content_dict:
		messege=f"\n検索条件名：{alert_content['検索条件名']}\n" \
						f"タイトル：{alert_content['タイトル']}\n" \
						f"価格：{alert_content['価格']}\n" \
						f"商品URL：{alert_content['商品URL']}"
		# f"商品説明文：{alert_content['商品説明文']}\n"
		send_line_notify(line_notify_token,messege,alert_content['画像URL'])
	send_line_notify(line_notify_token,pipe,'')
# LINE notify で送信する前処理
def final_process(update_url_list,self,site_type):
	# self.stdout.write(str(f'更新されたURL len({len(update_url_list)})\n{update_url_list}\n\n'))
	db_all_data_dict=get_db_all_data()
	if db_all_data_dict:
		if site_type=='kitamura':
			items_detail_dict=update_url_list
		elif site_type=='netmall':
			items_detail_dict=get_detail_netmall(update_url_list)
		alert_content_dict=get_filter_judge(db_all_data_dict,items_detail_dict,self)
		self.stdout.write(str(f'通知する内容\n{alert_content_dict}\n\n'))
		if alert_content_dict:
			send_alert_content(alert_content_dict)
	else:
		self.stdout.write(str(f'通知が全てOFFだったので通知しなかった\n\n'))

# ------------------------------
# その他
# ------------------------------
# DBの検索条件を取得
def get_db_all_data():
	db_all_data_dict=[]
	for sqm_obj in SearchQueryModel.objects.all():
		if sqm_obj.md_alert_sw=='checked':
			db_all_data_dict.append({'検索条件名':sqm_obj.md_query_name,
											'ORタイトル':sqm_obj.md_or_title,
											'除外タイトル':sqm_obj.md_ex_title,
											'OR商品説明文':sqm_obj.md_or_desc,
											'除外商品説明文':sqm_obj.md_ex_desc,
											'最低価格':sqm_obj.md_price_min,
											'最高価格':sqm_obj.md_price_max,
											})
	return db_all_data_dict
# selenium設定
def boot_selenium():
	chrome_options=webdriver.ChromeOptions()
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option("excludeSwitches",['enable-automation',
																														'enable-logging'])
	# chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
	chrome_options.add_argument('--headless')  #ヘッドレスモード
	chrome_options.add_argument('--incognito')  #シークレットモード
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-desktop-notifications')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--single-process')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--user-agent=aheahe')
	chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像を非表示
	# chrome_options.add_argument('--remote-debugging-port=9222') #
	chrome_options.page_load_strategy='none' #
	driver=webdriver.Chrome(options=chrome_options)
	# driver.maximize_window()
	return driver
# 検索条件と比較して全てOKなら items_detail_dict に検索条件名を付加して返す
def get_filter_judge(db_all_data_dict,items_detail_dict,self):
	alert_content_dict=[]
	for db_all_data in db_all_data_dict:
		for items_detail in items_detail_dict:
			filter_judge=[]
			# ORタイトル のフィルタ
			for filter_data in db_all_data['ORタイトル'].split(' '):
				if filter_data in items_detail['タイトル'] or db_all_data['ORタイトル']=='':
					filter_judge.append("OK")
					break
			else:
				filter_judge.append("NG")
			# 除外タイトル のフィルタ
			for filter_data in db_all_data['除外タイトル'].split(' '):
				if db_all_data['除外タイトル']=='':
					filter_judge.append("OK")
					break
				if filter_data in items_detail['タイトル']:
					filter_judge.append("NG")
					break
			else:
				filter_judge.append("OK")
			# OR商品説明文 のフィルタ
			for filter_data in db_all_data['OR商品説明文'].split(' '):
				if filter_data in items_detail['商品説明文'] or db_all_data['OR商品説明文']=='':
					filter_judge.append("OK")
					break
			else:
				filter_judge.append("NG")
			# 除外商品説明文 のフィルタ
			for filter_data in db_all_data['除外商品説明文'].split(' '):
				if db_all_data['除外商品説明文']=='':
					filter_judge.append("OK")
					break
				if filter_data in items_detail['商品説明文']:
					filter_judge.append("NG")
					break
			else:
				filter_judge.append("OK")
			# 価格 のフィルタ
			if db_all_data['最低価格']=='':
				min_price=0
			else:
				min_price=int(db_all_data['最低価格'])
			if db_all_data['最高価格']=='':
				max_price=sys.maxsize
			else:
				max_price=int(db_all_data['最高価格'])
			if min_price <= int(re.sub(r'[(税込)¥円,]','',items_detail['価格'])) <= max_price:
				filter_judge.append("OK")
			else:
				filter_judge.append("NG")
			# filter_judgeにNGが含まれていなければappendする
			if "NG" not in filter_judge:
				items_detail['検索条件名']=db_all_data['検索条件名']
				# dict を append するとなぜか 検索条件名 が上書きされるので以下の記事を参考にした
				# https://gist.github.com/dogrunjp/9748789
				alert_content_dict.append(items_detail.copy())
			self.stdout.write(str(f'db_all_data\n{db_all_data}\n'
														f'items_detail\n{items_detail}\n'
														f'filter_judge\n{filter_judge}\n\n'))
		# self.stdout.write(str(f'alert_content_dict\n{alert_content_dict}\n\n'))
	return alert_content_dict

# ------------------------------
# 新着を検出して通知を行う
# ------------------------------
def main_process(self):
	# kitamura
	while_count_kitamura=0
	old_url_list_kitamura=get_url_list_kitamura()
	# netmall
	while_count_netmall=0
	old_url_list_netmall=get_url_list_netmall()
	while True:
		# kitamura
		while_count_kitamura+=1
		new_url_list_kitamura=get_url_list_kitamura()
		update_url_list_kitamura=list(set(new_url_list_kitamura[:50])-set(old_url_list_kitamura))
		if update_url_list_kitamura:
			self.stdout.write(str(f'kitamura で更新されたURLの数：\n{len(update_url_list_kitamura)}\n\n'))
			while_count_kitamura=0
			old_url_list_kitamura=new_url_list_kitamura
			final_process(update_url_list_kitamura,self,'kitamura')
		else:
			self.stdout.write(str(f'{while_count_kitamura} 更新前の最新の kitamura のURL\n{old_url_list_kitamura[0]}\n\n'))
		# netmall
		while_count_netmall+=1
		new_url_list_netmall=get_url_list_netmall()
		update_url_list_netmall=list(set(new_url_list_netmall[:45])-set(old_url_list_netmall))
		if update_url_list_netmall:
			self.stdout.write(str(f'netmall で更新されたURLの数：\n{len(update_url_list_netmall)}\n\n'))
			while_count_netmall=0
			old_url_list_netmall=new_url_list_netmall
			final_process(update_url_list_netmall,self,'netmall')
		else:
			self.stdout.write(str(f'{while_count_netmall} 更新前の最新の netmall のURL\n{old_url_list_netmall[0]}\n\n'))
# キタムラのリニューアルに合わせて改良
def main_process_v2(self):
	# selenium を起動
	driver=boot_selenium()
	# エラーで終了しても driver.quit() 出来るように追加
	try:
		self.stdout.write(str(f'selenium 起動完了'))
		# kitamura
		while_count_kitamura=0
		old_detail_dict_kitamura=get_detail_kitamura_selenium(driver)
		# netmall
		while_count_netmall=0
		old_url_list_netmall=get_url_list_netmall()
		while True:
			# kitamura
			while_count_kitamura+=1
			new_detail_dict_kitamura=get_detail_kitamura_selenium(driver)
			update_detail_dict_kitamura=compare_detail_dict_kitamura(old_detail_dict_kitamura,new_detail_dict_kitamura)
			if update_detail_dict_kitamura:
				# winsound.Beep(1500,500)
				# winsound.Beep(1500,500)
				self.stdout.write(str(f'kitamura で更新されたURLの数：{len(update_detail_dict_kitamura)}\n\n'))
				while_count_kitamura=0
				old_detail_dict_kitamura=new_detail_dict_kitamura
				final_process(update_detail_dict_kitamura,self,'kitamura')
				# ------------------------------
				# break
				# ------------------------------
			else:
				self.stdout.write(str(f'{while_count_kitamura} 更新前の最新の kitamura のURL\n{old_detail_dict_kitamura[0]["商品URL"]}\n\n'))
			# netmall
			while_count_netmall+=1
			new_url_list_netmall=get_url_list_netmall()
			update_url_list_netmall=list(set(new_url_list_netmall[:45])-set(old_url_list_netmall))
			if update_url_list_netmall:
				# winsound.Beep(1500,500)
				# winsound.Beep(1500,500)
				self.stdout.write(str(f'netmall で更新されたURLの数：{len(update_url_list_netmall)}\n\n'))
				while_count_netmall=0
				old_url_list_netmall=new_url_list_netmall
				final_process(update_url_list_netmall,self,'netmall')
				# ------------------------------
				# break
				# ------------------------------
			else:
				self.stdout.write(str(f'{while_count_netmall} 更新前の最新の netmall のURL\n{old_url_list_netmall[0]}\n\n'))
	finally:
		self.stdout.write(str(f'異常終了したので driver.quit()'))
		driver.quit()
#
def main_process_netmall_only(self):
	# selenium を起動
	driver=boot_selenium()
	# エラーで終了しても driver.quit() 出来るように追加
	try:
		self.stdout.write(str(f'selenium 起動完了'))
		# netmall
		while_count_netmall=0
		old_url_list_netmall=get_url_list_netmall()
		while True:
			# netmall
			while_count_netmall+=1
			new_url_list_netmall=get_url_list_netmall()
			update_url_list_netmall=list(set(new_url_list_netmall[:45])-set(old_url_list_netmall))
			if update_url_list_netmall:
				# winsound.Beep(1500,500)
				# winsound.Beep(1500,500)
				self.stdout.write(str(f'netmall で更新されたURLの数：{len(update_url_list_netmall)}\n\n'))
				while_count_netmall=0
				old_url_list_netmall=new_url_list_netmall
				final_process(update_url_list_netmall,self,'netmall')
				# ------------------------------
				# break
				# ------------------------------
			else:
				self.stdout.write(str(f'{while_count_netmall} 更新前の最新の netmall のURL\n{old_url_list_netmall[0]}\n\n'))
	finally:
		self.stdout.write(str(f'異常終了したので driver.quit()'))
		driver.quit()


# https://qiita.com/jansnap/items/d50f59dabc5da7c1d0dd
class Command(BaseCommand):
	help = 'crawler for test.'
	def handle(self, *args, **options):
		'''SearchQueryModel.objects.create(id=1,md_query_name=datetime.datetime.now())
		while True:
			tmp_db=SearchQueryModel.objects.get(id=1)
			dt_now=datetime.now()
			tmp_db.md_query_name=dt_now
			self.stdout.write(str(dt_now))
			tmp_db.save()
			time.sleep(1)'''

		# main_process(self)
		# main_process_v2(self)
		main_process_netmall_only(self)

		# update_url_list=['https://www.net-chuko.com/buy/detail.do?ac=2142330109249',
		# 								 'https://www.net-chuko.com/buy/detail.do?ac=2145260095408']
		# items_detail_dict=get_detail_kitamura(update_url_list,self)
		# db_all_data_dict=get_db_all_data()
		# get_filter_judge(db_all_data_dict,items_detail_dict,self)
		# # self.stdout.write(str(f'{}\n\n'))
