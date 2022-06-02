import socket
import logging
import re
import time
from emoji import demojize


server = 'irc.chat.twitch.tv'
port = 80
nickname = 'karupasu1919'
token = 'oauth:pestt6kbf2w5i8nhuvibaudo3ha3ee'
channel = '#daiantsuda514'
# formatter = '%(asctime)s - %(message)s'
# logging.basicConfig(level=logging.DEBUG, format=formatter)

def main():
	sock = socket.socket()
	sock.connect((server, port))
	sock.send(f"CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands\r\n".encode('utf-8'))
	sock.send(f"PASS {token}\r\n".encode('utf-8'))
	sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
	sock.send(f"JOIN {channel}\r\n".encode('utf-8'))
	word_counter = 0
	patterns = ['モンキー']
	try:
		while True:
			time.sleep(0.1)
			resp = sock.recv(2048).decode('utf-8')
			word_list = []
			if resp.startswith('PING'):
				# sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
				sock.send("PONG\n".encode('utf-8'))
			elif len(resp) > 0:
				# resp = demojize(resp)
				# index = resp.rfind(' :')
				# chat = resp[index:]
				print(resp)
				# for pattern in patterns:
				# 	word = re.findall(pattern,chat)
				# 	[word_list.append(i) for i in word if len(word) >0]
				# if len(word_list) >0:
				# 	logging.info(chat)
				# 	word_counter += len(word_list)
				# 	print(word_list)
				# 	print(word_counter)

	except KeyboardInterrupt:
		sock.close()
		exit()

main()
