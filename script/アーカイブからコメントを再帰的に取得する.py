import json
import math

import requests

# 本来はもうAPIを使用してアーカイブのコメントは取得できないが、Twitch自身のclient_idを使用することで現在でも取得可能だがグレーな方法
# https://ja.stackoverflow.com/questions/83617/twitch-api-を用いてアーカイブ動画のコメントを取得したい
client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
video_id = '1465735012'

# 動画の長さ(秒)を取得
url = 'https://api.twitch.tv/v5/videos/' + video_id
headers = {'client-id': client_id}
r = requests.get(url, headers=headers)
video_data = r.json()
video_length=video_data['length']
# print(json.dumps(video_data, indent=2))

ts_chat_dist=[]

#
while True:
	try:
		url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor=' + ts_chat_data['_next']
	except:
		url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?content_offset_seconds=0'

	headers = {'client-id': client_id}
	r = requests.get(url, headers=headers)
	ts_chat_data = r.json()
	# print(row_data)

	# tsとchatを辞書型リストに格納
	ts_chat_dist+=[ {'ts':comment['content_offset_seconds'], 'chat':comment['message']['body'] } for comment in ts_chat_data['comments'] ]
	# print(ts_chat_dist)

	# 進捗を計算
	last_ts=ts_chat_dist[-1]['ts']
	progress=math.floor(int(last_ts)/int(video_length)*100)
	print(f'進捗：{progress}%')

	if '_next' not in ts_chat_data:
		break

# print(json.dumps(ts_chat_dist, indent=2))
print(ts_chat_dist)