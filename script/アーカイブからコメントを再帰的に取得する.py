import json
import math
import requests
from datetime import datetime as dt
import datetime



# 本来はもうAPIを使用してアーカイブのコメントは取得できないが、Twitch自身のclient_idを使用することで現在でも取得可能だがグレーな方法
# https://ja.stackoverflow.com/questions/83617/twitch-api-を用いてアーカイブ動画のコメントを取得したい
client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
headers = {'client-id': client_id}
video_id = '1465735012'



def main():
	# APIでアーカイブの諸データを取得
	url = 'https://api.twitch.tv/v5/videos/' + video_id
	r = requests.get(url, headers=headers)
	video_data = r.json()
	# 長さ(秒)
	video_length=video_data['length']
	# タイトル
	video_title=video_data['title']
	# print(video_title)
	# print(json.dumps(video_data, indent=2))

	ts_chat_dist=[]

	while True:
		try:
			url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor=' + ts_chat_data['_next']
		except:
			url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?content_offset_seconds=0'

		r = requests.get(url, headers=headers)
		ts_chat_data = r.json()
		# print(row_data)

		# tsとchatを辞書型リストに格納
		# tsは小数点以下も含まれることがあるので切り捨て
		# 経過時間をhh:mm:ss形式に変換
		ts_chat_dist+=[{'ts':str(datetime.timedelta(seconds=math.floor(int(comment['content_offset_seconds'])))),'chat':comment['message']['body']} for comment in ts_chat_data['comments'] ]
		print(ts_chat_dist)

		# 進捗を計算
		last_ts_hhmmss=dt.strptime(ts_chat_dist[-1]['ts'],'%H:%M:%S')
		last_ts=last_ts_hhmmss.hour*60*60+last_ts_hhmmss.minute*60+last_ts_hhmmss.second
		print(last_ts)
		progress=math.floor(int(last_ts)/int(video_length)*100)
		print(f'進捗：{progress}%')

		if '_next' not in ts_chat_data:
			break

		###
		# return
		###

	# print(json.dumps(ts_chat_dist, indent=2))
	# print(ts_chat_dist)

main()