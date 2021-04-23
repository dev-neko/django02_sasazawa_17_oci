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

# ------------------------------
# その他
# ------------------------------
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
	"""
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--remote-debugging-port=9222')
	"""
	# chrome_options.add_argument('--remote-debugging-port=9222') #
	# chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
	driver=webdriver.Chrome(options=chrome_options)
	# driver.maximize_window()
	return driver
# LINEとメールの通知用に整理
def get_excel_parser(excel_contents):
	ex_str="\n"
	for i in excel_contents:
		for count,n in enumerate(i):
			if count==len(i)-1:
				ex_str=ex_str+"開放予定日："+n+"\n"
			else:
				ex_str=ex_str+n+"\n"
		ex_str=ex_str+"\n"
	ex_str=ex_str.rstrip("\n")
	return ex_str
# メールの送信
def outlook_mail_send_smtp_starttls(to_email,subject,message):
	from email.mime.text import MIMEText
	import smtplib
	try:
		# SMTP認証情報
		account="j9fz5w65j2e9hkl2bn3q@outlook.com"
		password="e9j7c25w6E6l63qsUv3K"

		# 送受信先
		from_email=account

		# MIMEの作成
		msg=MIMEText(message,"plain")
		msg["Subject"]=subject
		msg["To"]=to_email
		msg["From"]=from_email

		# メール送信処理
		server=smtplib.SMTP("smtp.office365.com",587)
		server.starttls()
		server.login(account,password)
		server.send_message(msg)
		server.quit()
	except:
		pass
# LINEで通知を送信する、画像サムネイル表示も可能
def send_line_notify(token,message,image):
	line_notify_api = 'https://notify-api.line.me/api/notify'
	headers = {'Authorization': f'Bearer {token}'}
	data = {'message': message,
					'imageFullsize':image,
					'imageThumbnail':image}
	requests.post(line_notify_api, headers=headers, data=data)

# ------------------------------
#
# ------------------------------
def main_process_selenium_test(self):
	# selenium を起動
	driver=boot_selenium()
	self.stdout.write(str(f'selenium 起動完了'))
	# エラーで終了しても driver.quit() 出来るように追加
	try:
		selenium_sazanka(driver,self)
	finally:
		self.stdout.write(str(f'終了したので driver.quit()'))
		driver.quit()
#
def selenium_sazanka(driver,self):
	# キャンセル枠公開ページを開く
	url="https://www.yoyaku-sports.city.suginami.tokyo.jp/reselve/m_index.do"
	driver.get(url)
	driver.find_element_by_xpath("//*[text()='開放予定の案内']").click()
	Select(driver.find_element_by_name("prptyp")).select_by_visible_text("屋外テニス系")
	driver.find_element_by_name('submit').click()
	Select(driver.find_element_by_name("prpcod")).select_by_visible_text("テニス（硬式）")
	driver.find_element_by_name('submit').click()

	# 内容取得・整理
	tmp_list=[]
	excel_list=[]
	while True:
		bs4obj=bs4.BeautifulSoup(driver.page_source,'html.parser')
		cb_data=bs4obj.find("form",attrs={'name':'searchObjForm'}).text.split()
		for count,i in enumerate(cb_data):
			if count>5 and i not in "次前" and i not in "[開放予定日]":
				tmp_list.append(re.sub(r'[◇・\s]','',i))
				if (count-5)%6==0:
					excel_list.append(tmp_list)
					tmp_list=[]
		try:
			driver.find_element_by_xpath("//*[text()='次']").click()
		except NoSuchElementException:
			break
	driver.quit()
	self.stdout.write(str(f'オリジナルの内容：{excel_list}'))

	# 9時00分～19時00分 が含まれていた場合は5つの時間帯に修正
	except_time_list=['9時00分～11時00分','11時00分～13時00分','13時00分～15時00分','15時00分～17時00分','17時00分～19時00分']
	for c1,i in enumerate(excel_list):
		if '9時00分～19時00分' in i[3]:
			for c2,except_time in enumerate(except_time_list):
				excel_list[c1+c2][3]=except_time
			break
	self.stdout.write(str(f'複数の時間を整理した内容：{excel_list}'))

	# DBにキャンセル予定枠を保存、同時に予約する枠を削除
	BorderDataModel.objects.update_or_create(md_name='border data',
																					 defaults={'md_cancel_border':excel_list,
																										 'md_reserve_border':''})

	# LINEとメールの通知用に整理した内容を取得
	excel_parser=get_excel_parser(excel_list)
	# self.stdout.write(str(f'整理した内容：{excel_parser}'))
	# LINEトークンをDBから取得
	try:
		user_data=UserDataModel.objects.get(md_name='user data')
		line_token=user_data.md_line_token
		self.stdout.write(str(f'DBから取得したLINEトークン：{line_token}'))
		# 送信先のメールアドレスをDBから取得
		to_email=user_data.md_to_email
		self.stdout.write(str(f'DBから取得したメールアドレス：{to_email}'))
	except:
		self.stdout.write(str(f'UserDataModelが空なので通知しなかった'))
		line_token=to_email=''
	# LINE に通知
	send_line_notify(line_token,excel_parser,'')
	# メールアドレス に通知
	subject='さざんかねっと キャンセル枠開放スケジュール'
	outlook_mail_send_smtp_starttls(to_email,subject,excel_parser)







# https://qiita.com/jansnap/items/d50f59dabc5da7c1d0dd
class Command(BaseCommand):
	help = 'crawler for test.'
	def handle(self, *args, **options):

		main_process_selenium_test(self)