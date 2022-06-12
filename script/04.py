import requests
import json
import csv

# 本来はもうAPIを使用してアーカイブのコメントは取得できないが、Twitch自身のclient_idを使用することで現在でも取得可能だがグレーな方法
# https://ja.stackoverflow.com/questions/83617/twitch-api-を用いてアーカイブ動画のコメントを取得したい
client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
video_id = '1266540849'

# 一回目のリクエスト
url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?content_offset_seconds=0'
headers = {'client-id': client_id}
r = requests.get(url, headers=headers)
# print(r)
row_data = r.json()
# print(row_data)

# for comment in row_data['comments']:
# 	ts=comment['content_offset_seconds']
# 	chat=comment['message']['body']
# 	print(ts,chat)

ts_chat_dict=[ {'ts':comment['content_offset_seconds'], 'chat':comment['message']['body'] } for comment in row_data['comments'] ]
print(ts_chat_dict)
print(row_data['_next'])






# 二回目以降のリクエスト
# while '_next' in row_data:
# 	url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor=' + row_data['_next']
# 	headers = {'client-id': client_id}
# 	r = requests.get(url, headers=headers)
# 	row_data = r.json()
#
# 	for comment in row_data['comments']:
# 		ts=comment['content_offset_seconds']
# 		chat=comment['message']['body']
# 		print(ts,chat)
