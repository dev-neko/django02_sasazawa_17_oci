import json
import requests

# 本来はAPIを使用してアーカイブのコメントは取得できなくなったが、Twitch自身のclient_idを使用することでグレーな方法だが現在でも取得可能
# https://ja.stackoverflow.com/questions/83617/twitch-api-を用いてアーカイブ動画のコメントを取得したい
client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
headers = {'client-id': client_id}
# https://www.twitch.tv/videos/1465735012 の内の数字の部分だけを入力
video_id = '1465735012'

def main():
	# アーカイブの諸データを取得
	url = 'https://api.twitch.tv/v5/videos/' + video_id
	r = requests.get(url, headers=headers)
	video_data = r.json()

	# タイムスタンプとチャットを格納する辞書型リスト
	ts_chat_dist=[]

	while True:
		# 2回目以降のリクエスト
		try:
			url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor=' + ts_chat_data['_next']
		# 1回目のリクエスト
		except:
			url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?content_offset_seconds=0'

		# コメント類の諸データを取得
		r = requests.get(url, headers=headers)
		ts_chat_data = r.json()

		# タイムスタンプとチャットを辞書型リストに格納して後ろに結合
		ts_chat_dist+=[{'ts':comment['content_offset_seconds'],'chat':comment['message']['body']} for comment in ts_chat_data['comments'] ]

		# _nextトークンがなくなったら終了
		if '_next' not in ts_chat_data:
			break

	# アーカイブの諸データとタイムスタンプとチャットの辞書型リストを返す
	return video_data,ts_chat_dist

if __name__=='__main__':
	video_data,ts_chat_dist=main()
	# アーカイブの諸データ
	print(json.dumps(video_data, indent=2, ensure_ascii=False))
	# タイムスタンプとチャットの辞書型リスト
	print(json.dumps(ts_chat_dist, indent=2, ensure_ascii=False))
	# 長さ(秒)
	print(video_data['length'])
	# タイトル
	print(video_data['title'])