import re
import sys
import time
# import winsound
from datetime import datetime
from selenium import webdriver
from applications.models import UserDataModel,BorderDataModel
from django.core.management.base import BaseCommand, CommandError
import bs4,requests
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# selenium設定
def boot_selenium():
	chrome_options=webdriver.ChromeOptions()
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option("excludeSwitches",['enable-automation',
																														'enable-logging'])
	chrome_options.add_argument('--headless')  #ヘッドレスモード
	chrome_options.add_argument('--incognito')  #シークレットモード
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-desktop-notifications')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument('--disable-dev-shm-usage') #/dev/shmを使わないように指定
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--single-process')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--user-agent=aheahe')
	chrome_options.add_argument('--blink-settings=imagesEnabled=false') #画像を非表示
	chrome_options.page_load_strategy='none' #
	driver=webdriver.Chrome(options=chrome_options)
	return driver
