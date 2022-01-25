import pprint
import subprocess
import sys
import time
import datetime
import tkinter
from tkinter import messagebox

import bs4
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import re

# selenium設定
def boot_selenium():
	chrome_options=webdriver.ChromeOptions()
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
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
	chrome_options.page_load_strategy='none' #
	driver=webdriver.Chrome(options=chrome_options,executable_path=r"C:\Users\YUTANAO\PycharmProjects\PythonApps\camera_shop_alert_003\chromedriver.exe")
	# driver.maximize_window()
	return driver

def get_detail_kitamura_selenium(driver):
	items_detail_dict=[]
	add_url='https://www.net-chuko.com'
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

driver=boot_selenium()
print('ブラウザ起動完了')
for i in range(6):
	perf_start=time.perf_counter()
	old_detail_dict_kitamura=get_detail_kitamura_selenium(driver)
	perf_end=time.perf_counter()
	# pprint.pprint(old_detail_dict_kitamura)
	print(f"実行時間：{perf_end-perf_start}")

driver.quit()