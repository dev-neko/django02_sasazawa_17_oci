# ------------------------------
# ライブラリ
# ------------------------------
import os
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# chromedriver.exeのインストール先
CDM_INST=ChromeDriverManager().install()

# ------------------------------
# selenium
# ------------------------------
def selenium_driver(CDM_INST):
	chrome_options=webdriver.ChromeOptions()
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option('detach',True)
	chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
	# chrome_options.add_argument('--headless')  #ヘッドレスモード
	chrome_options.add_argument('--incognito')  #シークレットモード
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-desktop-notifications')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--ignore-certificate-errors')
	# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
	# chrome_options.page_load_strategy='none'
	# 2021年12月30日追加
	# chrome_options.add_argument('--allow-running-insecure-content')
	# chrome_options.add_argument('--disable-web-security')
	# chrome_options.add_argument('--lang=ja')
	# chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像非表示
	# Herokuではビルドパックが無いと動作しないし、CDM_INSTを指定していても動作しないので、tryで分岐して両対応
	try:
		return webdriver.Chrome(CDM_INST,options=chrome_options)
	except:
		return webdriver.Chrome(options=chrome_options)

def reserve(CDM_INST):
	def pre_reserve():
		# 事前手続き開始
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		return driver
	def aft_reserve(driver):
		url='https://setagaya.keyakinet.net/mobile/'
		driver.get(url)

	driver=pre_reserve()
	aft_reserve(driver)

reserve(CDM_INST)