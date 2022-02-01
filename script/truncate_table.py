# ------------------------------
# ライブラリ
# ------------------------------
import heroku3
import psycopg2
from psycopg2.extras import DictCursor

# ------------------------------
# HerokuDB操作
# ------------------------------
class postgres:
	# 接続時の設定
	def connection(self,HEROKU_API,HEROKU_APP_NAME):
		heroku_conn=heroku3.from_key(HEROKU_API)
		app=heroku_conn.app(HEROKU_APP_NAME)
		config=app.config()
		conn=psycopg2.connect(config['DATABASE_URL'])
		conn.autocommit=True
		cursor=conn.cursor()
		self.dictcur=conn.cursor(cursor_factory=DictCursor)
	# 指定したテーブルのすべての内容を辞書に変換して取得
	def fetchall_bdm_dict(self):
		self.dictcur.execute('SELECT * FROM applications_borderdatamodel')
		return [dict(r) for r in self.dictcur.fetchall()]
	# テーブルの内容をすべて消去
	def truncate_table(self):
		self.dictcur.execute('TRUNCATE TABLE applications_borderdatamodel')

HEROKU_API='c8c9dc16-f5c6-4e50-a9d7-33e1091ce94d'
HEROKU_APP_NAME='keyakinet008'

# HerokuのDBから予約内容を全て削除
def main():
	pg=postgres()
	pg.connection(HEROKU_API=HEROKU_API,HEROKU_APP_NAME=HEROKU_APP_NAME)
	pg.truncate_table()
	print('HerokuのDBから予約内容を全て削除しました。')
main()