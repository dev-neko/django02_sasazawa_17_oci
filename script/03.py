import datetime
import math
import re

resp='@badge-info=subscriber/4;badges=subscriber/3,moments/2;color=#8A2BE2;display-name=michako_gogo;emotes=;first-msg=0;flags=;id=ece40d85-254c-4f08-aa63-531c25963229;mod=0;room-id=216351084;subscriber=1;tmi-sent-ts=1654069719611;turbo=0;user-id=723424874;user-type= :michako_gogo!michako_gogo@michako_gogo.tmi.twitch.tv PRIVMSG #dasoku_aniki :メル「騙されたなぁ」'

d={ i.split('=')[0]:i.split('=')[1] for i in resp.split(';') }
# タイムスタンプを取得
ts = int(d['tmi-sent-ts'])
print(ts)
# チャットを取得
chat_resp = d['user-type']
chat = chat_resp[chat_resp.rfind(':')+1:]
print(chat)

dt = datetime.datetime.fromtimestamp(math.floor(ts/1000))
print(dt)
