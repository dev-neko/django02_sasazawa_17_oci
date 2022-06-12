import json
import math

import requests

# 本来はもうAPIを使用してアーカイブのコメントは取得できないが、Twitch自身のclient_idを使用することで現在でも取得可能だがグレーな方法
# https://ja.stackoverflow.com/questions/83617/twitch-api-を用いてアーカイブ動画のコメントを取得したい
client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
video_id = '1501683413'

# 動画の長さ(秒)を取得
url = 'https://api.twitch.tv/v5/videos/' + video_id
headers = {'client-id': client_id}
r = requests.get(url, headers=headers)
video_data = r.json()
video_length=video_data['length']
# print(json.dumps(video_data, indent=2))

# print(f'created_at:{video_data["created_at"]}')
# print(f'published_at:{video_data["published_at"]}')
# print(f'recorded_at:{video_data["recorded_at"]}')

# UTCなのでJSTにするために+9時間する
# recorded_at:2022-06-12T12:58:26Z

from datetime import datetime as dt
import datetime

video_recorded_at = video_data["recorded_at"]
tdatetime = dt.strptime(video_recorded_at, '%Y-%m-%dT%H:%M:%SZ')
print(tdatetime)

dt2 = tdatetime + datetime.timedelta(hours=9)
print(str(dt2))

dt2 = tdatetime + datetime.timedelta(seconds=30)
print(dt2)


