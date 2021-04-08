from __future__ import absolute_import, unicode_literals

import pprint
import re,bs4,requests
from celery import shared_task
import time



def tame01():
	items_url_list=[]
	# netmall カメラカテゴリ、新着順、90件表示
	src_url='https://netmall.hardoff.co.jp/cate/00010003/?p=1&s=1&pl=90'
	src_url_parser=requests.get(src_url)
	bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
	items_list=bs4obj.find_all("div",attrs={'class':'p-goods__item p-goods__item--with-cart-btn'})
	for items in items_list:
		# タイトル
		# items_title=items.find("span",attrs={'class':'p-goods__nameClamp'}).text
		# 価格
		# items_price=items.find("p",attrs={'class':'p-goods__price'}).text
		# 画像URL
		# items_imgurl=items.find("img",attrs={'class':'p-goods__img js-object-fit'}).get('src')
		# 商品URL
		items_url=items.find("a",attrs={'class':'p-goods__link'}).get('href')
		# 商品説明文
		# src_url_parser=requests.get(items_url)
		# bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# desc_list=bs4obj.find("div",attrs={'class':'p-goodsGuide__body'}).find_all("td")
		# items_desc=''
		# for desc in desc_list:
		# 	items_desc+=desc.text
		# print(items_url,items_title,items_price,items_imgurl,items_desc)
		items_url_list.append(items_url)
		# break
	# print(items_url_list)
	return items_url_list
# tame01()

def tame03():
	ListA=['a','b','c']
	ListB=['b','c','d','e']

	listC=list(set(ListB)-set(ListA))
	print(listC)
# tame03()

def tame04():
	a=['a','b','c']
	if len(a):
		print(a)
# tame04()

# netmall の「カメラカテゴリ、新着順、90件表示」で比較元のURLリストを取得
def tame05():
	items_url_list=[]
	src_url='https://netmall.hardoff.co.jp/cate/00010003/?p=1&s=1&pl=90'
	src_url_parser=requests.get(src_url)
	bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
	items_list=bs4obj.find_all("div",attrs={'class':'p-goods__item p-goods__item--with-cart-btn'})
	for items in items_list:
		# タイトル
		# items_title=items.find("span",attrs={'class':'p-goods__nameClamp'}).text
		# 価格
		# items_price=items.find("p",attrs={'class':'p-goods__price'}).text
		# 画像URL
		# items_imgurl=items.find("img",attrs={'class':'p-goods__img js-object-fit'}).get('src')
		# 商品URL
		items_url=items.find("a",attrs={'class':'p-goods__link'}).get('href')
		# 商品説明文
		# src_url_parser=requests.get(items_url)
		# bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# desc_list=bs4obj.find("div",attrs={'class':'p-goodsGuide__body'}).find_all("td")
		# items_desc=''
		# for desc in desc_list:
		# 	items_desc+=desc.text
		# print(items_url,items_title,items_price,items_imgurl,items_desc)
		items_url_list.append(items_url)
		# break
	# print(items_url_list)
	return items_url_list
# tame01()




# キタムラの「カテゴリ指定なし、更新日順、100件表示」でURLのリストを取得
# 比較先のURLリストはスライスして取得
def kitamura_get_url_list():
	items_url_list=[]
	add_url='https://www.net-chuko.com'
	src_url='https://www.net-chuko.com/buy/list.do?keyword=&ob=ud-&lc=100&pg=1'
	src_url_parser=requests.get(src_url)
	bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
	items_list=bs4obj.find_all("li",attrs={'class':'item-element'})
	for items in items_list:
		# 商品URL
		items_url=items.find("a",attrs={'class':'item-photo'}).get('href')
		items_url_list.append(add_url+items_url)
	# print(len(items_url_list))
	# print(items_url_list)
	return items_url_list

# キタムラの商品URLから必要な情報を取得
def kitamura_get_detail(update_url_list):
	items_detail_list=[]
	add_url='https://www.net-chuko.com'
	for update_url in update_url_list:
		src_url_parser=requests.get(update_url)
		bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# タイトル
		items_title=bs4obj.find("h1").text
		# 価格
		items_price=bs4obj.find("p",attrs={'class':'price'}).text
		# 画像URL
		items_imgurl=add_url+bs4obj.find("img",attrs={'id':'target'}).get('src')
		# 商品説明文
		th_list=bs4obj.find_all("th",attrs={'class':'contents'})
		for elem in th_list:
			if '備考' in str(elem.string):
				items_desc=elem.parent.find('td').text
				break
		items_detail_list.append({'タイトル':items_title,'価格':items_price,'画像URL':items_imgurl,'商品説明文':items_desc,'商品URL':update_url})
	# pprint.pprint(items_detail_list)
	return items_detail_list

# DBの検索条件と比較
def kitamura_comp_search_condi():
	'''タイトル検索でOR検索できること
	マイナス検索検索できること
	価格帯の絞り
	また、商品説明欄にも
	OR検索できること
	マイナス検索検索できること
	ができれば嬉しいです。(妥協可能です)'''
	db_data=[{'検索条件名':'aaa','ORタイトル':'あ い う','除外タイトル':'いい お','OR商品説明文':'あ い','除外商品説明文':'え お い','価格の絞り':''},]
	# or_title_str=
	# ex_title_str=
	# or_desc_str=
	# ex_desc_str=
	# price_filter=


# キタムラのURLを比較して新着を検出
def kitamura_comp_url():
	old_url_list=kitamura_get_url_list()
	while True:
		new_url_list=kitamura_get_url_list()
		update_url_list=list(set(new_url_list[:50])-set(old_url_list))
		if len(update_url_list):
			old_url_list=new_url_list
			items_detail_list=kitamura_get_detail(update_url_list)
			pprint.pprint(f'更新された商品：{items_detail_list}')
		else:
			print(f'更新前の最新の商品：{old_url_list[0]}')
		time.sleep(1)
# kitamura_comp_url()

# update_url_list=['https://www.net-chuko.com/buy/detail.do?ac=2142030137023&pp=a1-2','https://www.net-chuko.com/buy/detail.do?ac=2142030137146&pp=a1-2']
# items_detail_list=kitamura_get_detail(update_url_list)
# pprint.pprint(items_detail_list)
