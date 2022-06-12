import csv
import json

ts_chat_dist=[{'ts': 4, 'chat': 'お'}, {'ts': 4, 'chat': 'お'}, {'ts': 5, 'chat': 'おわた'}, {'ts': 5, 'chat': 'おおおおおおおおおおおおおおおお'}, {'ts': 5, 'chat': 'きたああああああああああああああああああああああああああああ'}, {'ts': 5, 'chat': 'あ'}, {'ts': 5, 'chat': 'BibleThump BibleThump'}, {'ts': 5, 'chat': '復活！！！'}, {'ts': 5, 'chat': 'ってことでね'}, {'ts': 5, 'chat': 'きた？'}]

# print(json.dumps(ts_chat_dist, indent=2))

with open('sample.csv', 'w', newline="") as f:
	writer = csv.DictWriter(f,['ts','chat'])
	writer.writeheader()
	writer.writerows(ts_chat_dist)

with open('sample.csv') as f:
	print(f.read())