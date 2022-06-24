import datetime
import math
import socket
import time

server = 'irc.chat.twitch.tv'
port = 80
# 自分のTwitchID 例:nickname = 'aabbcc'
nickname = ''
# 個別に取得したOAuth Token 例:token = 'oauth:aabbcc'
token = ''
# チャットを取得したいチャンネルIDの先頭に#を付与
channel = '#daiantsuda514'

def main():
	sock = socket.socket()
	sock.connect((server, port))

	# REQサブコマンドの指定
	sock.send(f"CAP REQ :twitch.tv/tags\r\n".encode('utf-8'))
	# OAuth Tokenの送信
	sock.send(f"PASS {token}\r\n".encode('utf-8'))
	# TwitchIDの送信
	sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
	# チャンネルIDの送信
	sock.send(f"JOIN {channel}\r\n".encode('utf-8'))

	# Ctrl+Cなどでの終了を待機
	try:
		while True:
			resp = sock.recv(2048).decode('utf-8')
			if resp.startswith('PING'):
				# 接続を継続させるために送信
				sock.send("PONG\n".encode('utf-8'))
			# 接続時の不要な文字列をpass
			elif (len(resp)>0) and ('PRIVMSG' in resp):
				# respを「;」区切りでリストに変換、そのリストの要素ごとに「=」区切りで辞書に変換
				resp_dict={i.split('=')[0]:i.split('=')[1] for i in resp.split(';')}
				# タイムスタンプを取得
				# タイムスタンプはミリ秒が含まれている13桁のUNIX時間のため、千で割って小数点以下を切り捨ててミリ秒部分を省き、年月日時分秒に変換
				ts=datetime.datetime.fromtimestamp(math.floor(int(resp_dict['tmi-sent-ts'])/1000))
				# チャットを取得
				# 最後にマッチするrfindを使用して、:の1つ後から最後までを取得
				chat_resp=resp_dict['user-type']
				chat=chat_resp[chat_resp.rfind(':')+1:]
				print(ts,chat)
			# 接続時の文字列を表示させたい場合
			else:
				# print(resp)
				pass
			# 念のためスリープ
			time.sleep(0.01)
	except KeyboardInterrupt:
			sock.close()
			exit()

if __name__=='__main__':
	main()