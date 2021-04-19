import pprint
import re,bs4,requests
import time



# netmallの「カメラカテゴリ、更新日順、90件表示」でURLのリストを取得
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

# netmallの商品URLから必要な情報を取得
def get_detail_netmall(update_url_list):
	items_detail_dict=[]
	add_url='https://netmall.hardoff.co.jp'
	for update_url in update_url_list:
		# self.stdout.write(str(f'update_url；\n{update_url}\n\n'))
		src_url_parser=requests.get(update_url)
		bs4obj=bs4.BeautifulSoup(src_url_parser.text,'html.parser')
		# タイトル
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
				items_desc+=elem.find('td').text.replace('　',' ')
		items_detail_dict.append({'タイトル':items_title,
															'価格':items_price,
															'画像URL':items_imgurl,
															'商品説明文':items_desc,
															'商品URL':update_url,
															})
	# print(items_detail_dict)
	# print(items_detail_dict[2]['商品説明文'])
	return items_detail_dict

update_url_list=['https://netmall.hardoff.co.jp/product/2192207/',
								 'https://netmall.hardoff.co.jp/product/2155800/',
								 'https://netmall.hardoff.co.jp/product/717368/']
a=get_detail_netmall(update_url_list)

for i in a:
	print(int(re.sub(r'[(税込)¥円,]','',i['価格'])))