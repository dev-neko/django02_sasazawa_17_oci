"""
参考
Twitchのコメントを取得して解析するプログラム - Qiita
https://qiita.com/takdcloose/items/71072649c455830af929
Twitch配信アーカイブのコメント流量を可視化してみた - Qiita
https://qiita.com/kanekom/items/42ed3cd079fa5409ae58

経過
2022年6月1日
ツイッチのAPIの動作確認をした
2022年6月2日
ライブからコメントとタイムスタンプを取得できるようになった
コメントの流れが速いと1個か2個くらい抜けてしまうが、概ね取得できることを確認した

nickname
karupasu1919
access_token
2uk2854x3r90a26l5aibi9csd8gzq2
client_id
gq5u9v47cfdorumns4qo8rfqyix2kv
token
oauth:pestt6kbf2w5i8nhuvibaudo3ha3ee
"""

import datetime
import math
import socket
import logging
import re
import time
# 絵文字処理
from emoji import demojize


server = 'irc.chat.twitch.tv'
port = 80
nickname = 'karupasu1919'
token = 'oauth:pestt6kbf2w5i8nhuvibaudo3ha3ee'
channel = '#killin9hit'

def main():
	sock = socket.socket()
	sock.connect((server, port))
	# tagsだけでタイムスタンプは取得可能だったので他は省略
	# sock.send(f"CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands\r\n".encode('utf-8'))
	sock.send(f"CAP REQ :twitch.tv/tags\r\n".encode('utf-8'))
	sock.send(f"PASS {token}\r\n".encode('utf-8'))
	sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
	sock.send(f"JOIN {channel}\r\n".encode('utf-8'))
	try:
		while True:
			time.sleep(0.01)
			resp = sock.recv(2048).decode('utf-8')
			if resp.startswith('PING'):
				# sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
				sock.send("PONG\n".encode('utf-8'))
			# 接続時の不要な文字列をpass
			elif (len(resp)>0) and ('PRIVMSG' in resp):
				# respを;区切りでリストに変換、そのリストの要素ごとに=区切りで辞書に変換
				d={ i.split('=')[0]:i.split('=')[1] for i in resp.split(';')}
				# タイムスタンプを取得
				# 返されるのはミリ秒が含まれているので千で割って小数点以下切り捨て
				ts=datetime.datetime.fromtimestamp(math.floor(int(d['tmi-sent-ts'])/1000))
				# チャットを取得
				# 最後にマッチするrfindを使用して、:の1つ後から最後までを取得
				chat_resp=d['user-type']
				chat=chat_resp[chat_resp.rfind(':')+1:]
				print(ts,chat)
			# 接続時の文字列を表示させたい場合
			else:
				pass
				print(resp)
	except KeyboardInterrupt:
			sock.close()
			exit()

main()