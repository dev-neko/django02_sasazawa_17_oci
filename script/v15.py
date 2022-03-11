"""
セレニで並列操作できるか確認
https://a-zumi.net/python-selenium-multithread/
↓
ポスグレからデータ取得してその内容で予約を行う
↓
ファイル容量を減らすためにmy_moduleで利用する関数を含めた
マイモ有り53mb、マイモ無し7mbだったのでマイモ無しにした
↓
コートの切り替えボタンをクリックし続けて、時間帯が表示され次第クリックする様に変更
↓
コートの切り替えボタンをクリックし続けて12時になっても時間帯が表示されなかったので室場選択画面で待機して、11時59分55秒になったらクリックするように変更
ChromeDriverManager().install()を2回連続で行うと失敗することがあるので1回のみで処理できるように変更
よく考えたら12時前にクリックしても時間帯が表示されなさそうなので、やっぱり12時00秒にクリックす量に変更
↓
複数の予約枠に対して、1つのIDを用いて、1つのセッション、これを2つのIDで行う
という形式に変更
↓
タイムアウト設定、予約結果の取得、except追加、予約後にデータ削除
↓
ログでIDを区別する文字を追加、実際に予約を行うかの分岐を追加、
↓
ヘッドレスにしただけ
↓
ヘッドレスにしても2021年12月30日の予約が出来なかったので少しでも早く予約できるようにプログラムを見直した
実際に予約を行わない場合はinfo表示
DEBUG、REAL_RESERVE、STR_TIMEも表示
useragent
画像非表示
sleniumオプション追加
↓
追加したseleniumオプションが影響しているのかは不明だが近頃予約が出来ていないので、とりあえず無効化した
↓
DEBUG=Trueだったら予約内容消さないようにした
↓
Herokuである程度まともに動くことが分かったので、DEBUGに関係なく予約内容消すようにした
ヘッドレスなのでウィンドウの処理削除した
要素が見つからない理由が分からなかったので、そのページの内容を表示させる処理を追加した
↓
Herokuでも多重ログインができないことが分かったので、2つのIDでそれぞれ1インスタンスで手続きするように変更
スレッド処理は削除

"""

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
from datetime import datetime
import heroku3
import psycopg2
from psycopg2.extras import DictCursor
import time

# ------------------------------
# 定数
# ------------------------------
DEBUG=True
# DEBUG=False

# 実際に予約を行うかの分岐 Trueで行う
REAL_RESERVE=True
# REAL_RESERVE=False

AC_ID_1='00836979'
AC_PW_1='12563986'
AC_ID_2='20094001'
AC_PW_2='01010101'

HEROKU_API='c8c9dc16-f5c6-4e50-a9d7-33e1091ce94d'
HEROKU_APP_NAME='keyakinet008'

# chromedriver.exeのインストール先
CDM_INST=ChromeDriverManager().install()

# この時間までスリープ
STR_TIME=datetime.strptime('12:00:00','%H:%M:%S').time()
PRE_TIME=datetime.strptime('11:40:00','%H:%M:%S').time()

# IDAとIDBで処理を分けるためにHerokuの環境変数を取得
SCRIPT_TYPE=os.environ.get('SCRIPT_TYPE')

# ------------------------------
# logger
# ------------------------------
"""------------------------------
DEBUG True 時は全てを表示するが、何も記録しない
DEBUG False 時は全てを記録するが、DEBUG内容は表示しない

# DEBUG=True
DEBUG=False
の追加も必要

# 大体全部
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(processName)s]-[%(filename)s]-[line:%(lineno)s]-[%(funcName)s]-[%(module)s]-[%(name)s]-[%(message)s]'
# DEBUG=True で良さそうな表示内容
str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
# DEBUG=False で良さそうな表示内容
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'

logger.debug('パスワード')
logger.info('予約内容')
logger.warning('予約指定が無いため終了します')
logger.error('見つからなかった要素')
------------------------------"""
def default_logging(DEBUG,log_file_name,str_format_ptn,file_format_ptn):
	import logging
	logger=logging.getLogger(__name__)
	if DEBUG:
		logger.setLevel(logging.DEBUG)
		str_handler=logging.StreamHandler()
		str_handler.setLevel(logging.DEBUG)
		str_format=logging.Formatter(str_format_ptn)
		str_handler.setFormatter(str_format)
		logger.addHandler(str_handler)
	else:
		logger.setLevel(logging.DEBUG)
		str_handler=logging.StreamHandler()
		str_handler.setLevel(logging.INFO)
		str_format=logging.Formatter(str_format_ptn)
		str_handler.setFormatter(str_format)
		logger.addHandler(str_handler)
		file_handler=logging.FileHandler(log_file_name+'.log')
		file_handler.setLevel(logging.DEBUG)
		file_format=logging.Formatter(file_format_ptn)
		file_handler.setFormatter(file_format)
		logger.addHandler(file_handler)
	# 区切りをあらかじめ付加しておく
	logger.debug('------------------------------------------------------------')
	return logger

str_format_ptn='[%(asctime)s]-[%(levelname)s]-[line:%(lineno)s]\n%(message)s'
file_format_ptn='[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[line:%(lineno)s]\n%(message)s'
logger=default_logging(DEBUG,'reserve',str_format_ptn,file_format_ptn)

# ------------------------------
# selenium
# ------------------------------
def selenium_driver(CDM_INST):
	chrome_options=webdriver.ChromeOptions()
	# アダプタエラー、自動テスト…、を非表示
	chrome_options.add_experimental_option('detach',True)
	chrome_options.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])
	chrome_options.add_argument('--headless')  #ヘッドレスモード
	chrome_options.add_argument('--incognito')  #シークレットモード
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--disable-desktop-notifications')
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument('--disable-dev-shm-usage')
	chrome_options.add_argument('--disable-application-cache')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--ignore-certificate-errors')
	# chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
	chrome_options.page_load_strategy='none'
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

# ------------------------------
# HerokuDB操作
# ------------------------------
class postgres:
	# 接続時の設定
	def connection(self,HEROKU_API,HEROKU_APP_NAME):
		self.heroku_conn=heroku3.from_key(HEROKU_API)
		self.app=self.heroku_conn.app(HEROKU_APP_NAME)
		self.config=self.app.config()
		self.conn=psycopg2.connect(self.config['DATABASE_URL'])
		self.conn.autocommit=True
		self.cursor=self.conn.cursor()
		self.dictcur=self.conn.cursor(cursor_factory=DictCursor)
	# 指定したテーブルのすべての内容を辞書に変換して取得
	def fetchall_bdm_dict(self):
		self.dictcur.execute('SELECT * FROM applications_borderdatamodel')
		return [dict(r) for r in self.dictcur.fetchall()]
	# テーブルの内容をすべて消去
	def truncate_table(self):
		self.dictcur.execute('TRUNCATE TABLE applications_borderdatamodel')

# ------------------------------
# main def
# ------------------------------
def test03(ac_id,ac_pass,CDM_INST,border_data,USEID):
	try:
		# 定数をまとめる
		R_DAY=datetime.strptime(border_data['md_r_day'],'%Y-%m-%d')
		R_NEN=R_DAY.year
		R_TSUKI=R_DAY.month
		R_HI=R_DAY.day
		R_TIME=border_data['md_r_time']
		R_SHISETSU=border_data['md_r_shisetsu']
		R_SHITSUJOU=border_data['md_r_shitsujou']
		R_CORDER=border_data['md_r_corder']
		# 事前手続き開始
		logger.info(f'{USEID}:{datetime.now().time()} になったため、ログインして事前手続きを開始します。')
		driver=selenium_driver(CDM_INST)
		# ページの読み込みで待機する秒数、これ以上経過すると例外発生
		driver.set_page_load_timeout(60)
		url='https://setagaya.keyakinet.net/mobile/'
		driver.get(url)
		logger.debug(f'{USEID}:{url} にアクセス')
		driver.find_element_by_xpath("//*[text()='けやきネット']").click()
		logger.debug(f'{USEID}:けやきネット')
		driver.find_element_by_xpath("//*[text()='ログインする']").click()
		logger.debug(f'{USEID}:ログインする')
		driver.execute_script('document.getElementsByName("txtUserID$txt")[0].value="%s";'%ac_id)
		logger.debug(f'{USEID}:ID入力')
		driver.execute_script('document.getElementsByName("txtPwd$txt")[0].value="%s";'%ac_pass)
		logger.debug(f'{USEID}:PASS入力')
		driver.find_element_by_xpath("//*[@value='[6]ログイン']").click()
		logger.debug(f'{USEID}:[6]ログイン')
		# 未読のメッセージがあればクリック
		try:
			driver.find_element_by_xpath("//*[@value='[6]次へ']").click()
			logger.debug(f'{USEID}:未読のメッセージが有ったのでクリック')
		except:
			logger.debug(f'{USEID}:未読のメッセージが無かったのでpass')
			pass
		# コート検索
		driver.find_element_by_xpath("//*[text()='使用目的から探す']").click()
		logger.debug(f'{USEID}:使用目的から探す')
		Select(driver.find_element_by_name("slPurpose1")).select_by_visible_text("屋外スポーツ")
		logger.debug(f'{USEID}:屋外スポーツ')
		driver.find_element_by_xpath("//*[@value='選択']").click()
		logger.debug(f'{USEID}:選択')
		# 使用目的の選択
		bs4obj=BeautifulSoup(driver.page_source,'html.parser')
		for input_elem in bs4obj.select('input[name="slPurpose2"]'):
			if input_elem.next_sibling=="テニス":
				input_name=input_elem.get('name')
				input_value=input_elem.get('value')
				driver.find_element_by_xpath("//input[@name='"+input_name+"'][@value="+input_value+"]").click()
				logger.debug(f'{USEID}:テニス が有ったので選択')
				break
		driver.find_element_by_xpath("//*[@value='[6]検索']").click()
		logger.debug(f'{USEID}:[6]検索')
		# 日付指定
		driver.execute_script('document.getElementsByName("txtNen$txt")[0].value="%s";'%R_NEN)
		logger.debug(f'{USEID}:{R_NEN}年')
		driver.execute_script('document.getElementsByName("txtTsuki$txt")[0].value="%s";'%R_TSUKI)
		logger.debug(f'{USEID}:{R_TSUKI}月')
		driver.execute_script('document.getElementsByName("txtHi$txt")[0].value="%s";'%R_HI)
		logger.debug(f'{USEID}:{R_HI}日')
		# 施設選択
		flag=False
		while True:
			bs4obj=BeautifulSoup(driver.page_source,'html.parser')
			for input_elem in bs4obj.select('input[name="slShisetsu"]'):
				if input_elem.next_sibling==R_SHISETSU:
					input_name=input_elem.get('name')
					logger.debug(f'{USEID}:input_name:{input_name}')
					input_value=input_elem.get('value')
					logger.debug(f'{USEID}:input_value:{input_value}')
					driver.find_element_by_xpath("//input[@name='"+input_name+"'][@value="+input_value+"]").click()
					logger.debug(f'{USEID}:{R_SHISETSU} が有ったので選択')
					flag=True
					break
			else:
				try:
					driver.find_element_by_xpath("//*[@value='[3]次頁']").click()
					logger.debug(f'{USEID}:[3]次頁')
				except:
					logger.error(f'{USEID}:{R_SHISETSU} が見つからなかったため終了')
					return
			# flagでwhileを抜ける
			if flag:
				break
		driver.find_element_by_xpath("//*[@value='[6]次へ']").click()
		logger.debug(f'{USEID}:[6]次へ')
		driver.find_element_by_link_text("[6]次へ").click()
		logger.debug(f'{USEID}:[6]次へ(リンク)')
		# 指定の時間までスリープ
		logger.info(f'{USEID}:事前手続きが完了したため、{STR_TIME}までスリープします。')
		while STR_TIME>=datetime.now().time():
			time.sleep(0.1)
		logger.info(f'{USEID}:{STR_TIME}を過ぎたため、予約手続きを再開します。')
		# 記号は無視して名称だけで部分一致で室場選択
		driver.find_element_by_partial_link_text(R_SHITSUJOU).click()
		logger.debug(f'{USEID}:{R_SHITSUJOU} を選択')
		# 時間選択
		try:
			Select(driver.find_element_by_name("slMen")).select_by_value(str(int(R_CORDER)-1))
			logger.debug(f'{USEID}:slMen')
			driver.find_element_by_xpath("//*[@value='切替']").click()
			logger.debug(f'{USEID}:切替')
			bs4obj=BeautifulSoup(driver.page_source,'html.parser')
			for input_elem in bs4obj.select('input[name="slTime"]'):
				if input_elem.next_sibling==R_TIME:
					input_name=input_elem.get('name')
					logger.debug(f'{USEID}:input_name:{input_name}')
					input_value=input_elem.get('value')
					logger.debug(f'{USEID}:input_value:{input_value}')
					driver.find_element_by_xpath("//input[@name='"+input_name+"'][@value="+input_value+"]").click()
					logger.debug(f'{USEID}:{R_TIME} が有ったので選択')
					driver.find_element_by_xpath("//*[@value='[6]申込へ']").click()
					logger.debug(f'{USEID}:[6]申込へ')
					break # for
			else:
				# forで最後まで見ても指定した時間がない場合は例外を発生させる
				raise Exception
		except Exception as err:
			# 時間が表示されなかった原因が分からなかったので追加→恐らく読み込み完了遅れ
			logger.error(f'Exceptionのエラー：{err}')
			logger.warning(f'{USEID}:{R_TIME} が表示されていないため終了します。')
			return
		# 使用目的
		Select(driver.find_element_by_name("slMokuteki")).select_by_visible_text("テニス")
		logger.debug(f'{USEID}:テニス')
		driver.find_element_by_xpath("//*[@value='[6]次へ']").click()
		logger.debug(f'{USEID}:[6]次へ')
		# 実際に予約を行うかの分岐
		if not REAL_RESERVE:
			logger.debug(f'{USEID}:REAL_RESERVEが{REAL_RESERVE}のため、予約は行いません。')
			return
		else:
			logger.debug(f'{USEID}:REAL_RESERVEが{REAL_RESERVE}のため、予約を行います。')
		# 最終確認
		driver.find_element_by_xpath("//*[@value='[6]申込']").click()
		logger.debug(f'{USEID}:[6]申込')
		# 結果取得
		res_result=BeautifulSoup(driver.page_source,'html.parser').text
		result_list=['予約申込を受付しました。',
								 '他の利用者によって予約されてしまいました。',
								 '大変申し訳ありませんが、システム処理中にエラーが発生いたしました。']
		for result in result_list:
			if result in res_result:
				logger.info(f'{USEID}:{result}')
				break
		else:
			logger.error(f'{USEID}:エラー発生時のソース\n{res_result}')
	except selenium.common.exceptions.TimeoutException:
		logger.warning(f'{USEID}:60秒間の読み込みが発生したためタイムアウトしました。')
	except selenium.common.exceptions.NoSuchElementException as err:
		logger.warning(f'{USEID}:見つからなかった要素\n{err}')
		# ページ内容取得
		res_result=BeautifulSoup(driver.page_source,'html.parser').text
		logger.warning(f'{USEID}:要素があったはずのページ内容\n{res_result}')
	except Exception as err:
		logger.error(err)
	finally:
		logger.info(f'{USEID}:予約処理が完了しました。')
		# driver.quit()

# ------------------------------
# main
# ------------------------------
def main03():
	# 定数の表示
	logger.debug(f'DEBUG:{DEBUG}')
	logger.debug(f'REAL_RESERVE:{REAL_RESERVE}')
	logger.debug(f'PRE_TIME:{PRE_TIME}')
	logger.debug(f'STR_TIME:{STR_TIME}')
	logger.debug(f'SCRIPT_TYPE:{SCRIPT_TYPE}')
	# HerokuのDBから予約内容を取得
	pg=postgres()
	pg.connection(HEROKU_API=HEROKU_API,HEROKU_APP_NAME=HEROKU_APP_NAME)
	bdm_dict=pg.fetchall_bdm_dict()
	# IDA→border_data_01、IDB→border_data_02にするための処理
	border_data_01=border_data_02=None
	for dict in bdm_dict:
		if 'border_data_01' in dict.values():
			border_data_01=dict
		if 'border_data_02' in dict.values():
			border_data_02=dict
	logger.debug(f'border_data_01:{border_data_01}')
	logger.debug(f'border_data_02:{border_data_02}')
	# IDごとに予約手続き開始
	if border_data_01 and (SCRIPT_TYPE=='IDA'):
		logger.info(f'IDAの予約枠の手続きを行います。')
		test03(AC_ID_1,AC_PW_1,CDM_INST,border_data_01,'IDA')
	elif border_data_02 and (SCRIPT_TYPE=='IDB'):
		logger.info(f'IDBの予約枠の手続きを行います。')
		test03(AC_ID_2,AC_PW_2,CDM_INST,border_data_02,'IDB')
	else:
		logger.warning(f'予約枠が登録されていないため終了します。')
		return

# Herokuスケジューラでは30分単位でしか指定できないため、指定の時間までスリープ
logger.info(f'プログラムは開始されましたが、{PRE_TIME}までスリープします。')
while PRE_TIME>=datetime.now().time():
	time.sleep(1)
logger.info(f'{PRE_TIME}を過ぎたため、事前手続きを開始します。')
main03()