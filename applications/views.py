import json
import math
import requests
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from .models import DBModel
from datetime import datetime as dt
import datetime



def input_v1(request):
	# ログインの確認
	if request.user.is_authenticated:
		TIME_DATA=['6:00～7:00',
							 '6:00～8:00',
							 '7:00～9:00',
							 '9:00～11:00',
							 '11:00～13:00',
							 '13:00～15:00',
							 '15:00～16:00',
							 '15:00～17:00',
							 '17:00～19:00',
							 '18:30～20:30',
							 '19:00～21:00',
							 '21:00～22:00']
		SHISETSU_DATA=['世田谷公園',
									 '羽根木公園',
									 '玉川野毛町公園',
									 '総合運動場',
									 '大蔵第二運動場',
									 'リコー砧総合運動場',
									 '烏山中学校',
									 '砧中学校',
									 '砧南中学校',
									 '桜丘中学校',
									 '瀬田中学校',
									 '玉川中学校',
									 '深沢中学校',
									 '三宿中学校',
									 '用賀中学校',
									 '芦花中学校']
		SHITUJOU_DATA=['庭球場',
									 '庭球場（照明付）',
									 '庭球場（照明なし）',
									 'テニスコート照明付',
									 'テニスコート照明なし']
		CORDER_DATA=[i for i in range(10)]
		# ページ読み込み時にDBのデータを読み込む
		try:
			border_data_01=BorderDataModel.objects.get(md_name='border_data_01')
			resp_01={'md_r_day':border_data_01.md_r_day,
										'md_r_time':border_data_01.md_r_time,
										'md_r_shisetsu':border_data_01.md_r_shisetsu,
										'md_r_shitsujou':border_data_01.md_r_shitsujou,
										'md_r_corder':border_data_01.md_r_corder,}
		except:
			resp_01={}
		try:
			border_data_02=BorderDataModel.objects.get(md_name='border_data_02')
			resp_02={'md_r_day':border_data_02.md_r_day,
										'md_r_time':border_data_02.md_r_time,
										'md_r_shisetsu':border_data_02.md_r_shisetsu,
										'md_r_shitsujou':border_data_02.md_r_shitsujou,
										'md_r_corder':border_data_02.md_r_corder,}
		except:
			resp_02={}
		json_resp={'resp_01':resp_01,'resp_02':resp_02}
		# print(json_resp)
		base_data={'TIME_DATA':TIME_DATA,
							 'SHISETSU_DATA':SHISETSU_DATA,
							 'SHITUJOU_DATA':SHITUJOU_DATA,
							 'CORDER_DATA':CORDER_DATA,
							 'json_resp':json_resp}
		return render(request, 'applications/input_v1.html', base_data)
	else:
		return HttpResponseRedirect('/accounts/login/')

def ajax_proc(request):
	if request.method=='POST':
		print(request.POST)
		post_data={'md_r_day':request.POST.get('r_day'),
							 'md_r_time':request.POST.get('r_time'),
							 'md_r_shisetsu':request.POST.get('r_shisetsu'),
							 'md_r_shitsujou':request.POST.get('r_shitsujou'),
							 'md_r_corder':request.POST.get('r_corder'),}
		# 保存ボタン 01
		if request.POST["db_action"]=="save_01":
			resp_db_action='save'
			BorderDataModel.objects.update_or_create(md_name='border_data_01',defaults=post_data)
			print(f'予約日を登録した 01')
		# 保存ボタン 02
		elif request.POST["db_action"]=="save_02":
			resp_db_action='save'
			BorderDataModel.objects.update_or_create(md_name='border_data_02',defaults=post_data)
			print(f'予約日を登録した 02')
		# 削除ボタン 01
		elif request.POST["db_action"]=="delete_01":
			resp_db_action='delete'
			# データが無いとerrorになるのでtry
			try:
				BorderDataModel.objects.get(md_name='border_data_01').delete()
			except:
				pass
			print(f'予約日を削除した 01')
		# 削除ボタン 02
		elif request.POST["db_action"]=="delete_02":
			resp_db_action='delete'
			# データが無いとerrorになるのでtry
			try:
				BorderDataModel.objects.get(md_name='border_data_02').delete()
			except:
				pass
			print(f'予約日を削除した 02')
		# DBのデータをすべて取得
		try:
			border_data_01=BorderDataModel.objects.get(md_name='border_data_01')
			resp_01={'md_r_day':border_data_01.md_r_day,
										'md_r_time':border_data_01.md_r_time,
										'md_r_shisetsu':border_data_01.md_r_shisetsu,
										'md_r_shitsujou':border_data_01.md_r_shitsujou,
										'md_r_corder':border_data_01.md_r_corder,}
		except:
			resp_01={}
		try:
			border_data_02=BorderDataModel.objects.get(md_name='border_data_02')
			resp_02={'md_r_day':border_data_02.md_r_day,
										'md_r_time':border_data_02.md_r_time,
										'md_r_shisetsu':border_data_02.md_r_shisetsu,
										'md_r_shitsujou':border_data_02.md_r_shitsujou,
										'md_r_corder':border_data_02.md_r_corder,}
		except:
			resp_02={}
		json_resp={'resp_01':resp_01,'resp_02':resp_02,'resp_db_action':resp_db_action}
	return JsonResponse(json_resp)

def userdata(request):
	if request.user.is_authenticated:
		return render(request, 'applications/userdata.html')
	else:
		return HttpResponseRedirect('/accounts/login/')

def ajax_proc_first(request):
	if request.method=='POST':
		# print(request.POST)
		post_data={'req_videoids':request.POST.get('videoids'),
		           }
		# print(post_data)

		client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
		video_id = post_data['req_videoids']
		# print(video_id)

		url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?content_offset_seconds=0'
		headers = {'client-id': client_id}
		r = requests.get(url, headers=headers)
		# print(r)
		row_data = r.json()
		# print(row_data)

		# tsとchatを辞書型リストに格納
		ts_chat_dist=[ {'timestamp(JST)':comment['content_offset_seconds'], 'chat':comment['message']['body'] } for comment in row_data['comments'] ]
		# print(ts_chat_dist)

		# DBに保存
		DBModel.objects.update_or_create(
			# ユニークな値
			md_name=video_id,
			# 更新もしくは新規で追加したい値
			defaults={'md_ts_chat':ts_chat_dist}
		)
		print(f'1回目のコメントとTSを登録した')

		json_resp={'ts_chat_dist':ts_chat_dist,
		           'video_id':video_id,
		           'next_token':row_data['_next'],
		           }

	return JsonResponse(json_resp)

def ajax_proc_after(request):
	if request.method=='POST':
		# print(request.POST)
		post_data={
			'req_videoids':request.POST.get('videoids'),
			'req_next_token':request.POST.get('next_token'),
		}
		# print(post_data)

		client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
		video_id = post_data['req_videoids']
		next_token= post_data['req_next_token']
		# print(video_id)

		url = 'https://api.twitch.tv/v5/videos/' + video_id + '/comments?cursor=' + next_token
		headers = {'client-id': client_id}
		r = requests.get(url, headers=headers)
		# print(r)
		row_data = r.json()
		# print(row_data)

		# tsとchatを辞書型リストに格納
		ts_chat_dist=[ {'timestamp(JST)':comment['content_offset_seconds'], 'chat':comment['message']['body'] } for comment in row_data['comments'] ]
		# print(ts_chat_dist)

		# DBに保存
		DBModel.objects.update_or_create(
			# ユニークな値
			md_name=video_id,
			# 更新もしくは新規で追加したい値
			defaults={'md_ts_chat':ts_chat_dist}
		)
		print(f'2回目以降のコメントとTSを登録した')

		try:
			json_resp={'ts_chat_dist':ts_chat_dist,
			           'video_id':video_id,
			           'next_token':row_data['_next'],
			           }
		except:
			json_resp={'ts_chat_dist':ts_chat_dist,
			           'video_id':video_id,
			           'next_token':'None',
			           }

	return JsonResponse(json_resp)





def ajax_proc_aaa(request):
	if request.method=='POST':
		# print(request.POST)
		post_data={
			'req_videoids':request.POST.get('videoids'),
			'req_next_token':request.POST.get('next_token'),
			'req_video_length':request.POST.get('video_length'),
			'req_video_recorded_at_jst':request.POST.get('video_recorded_at_jst'),
		}
		# print(post_data)

		client_id = 'kimne78kx3ncx6brgo4mv6wki5h1ko'
		headers = {'client-id': client_id}

		# 1回目はトークンがないので、それを利用してURLを分岐
		if post_data['req_next_token']==None:
			ts_chat_url = 'https://api.twitch.tv/v5/videos/' + post_data['req_videoids'] + '/comments?content_offset_seconds=0'
			# 同じvideoidで再取得するとdistが増え続けるので1回目にDBからvideoidを指定して全て削除
			try:
				DBModel.objects.get(md_name=post_data['req_videoids']).delete()
			except:
				pass
			# 1回目にAPIから動画の長さ(秒)と配信開始日時を取得
			video_data_url = 'https://api.twitch.tv/v5/videos/' + post_data['req_videoids']
			r = requests.get(video_data_url, headers=headers)
			video_data = r.json()
			# print(json.dumps(video_data, indent=2))
			# 動画の長さ(秒)
			video_length = video_data['length']
			# 日時オブジェクトに変換してJSTにするために+9時間
			video_recorded_at_jst=dt.strptime(video_data["recorded_at"],'%Y-%m-%dT%H:%M:%SZ')+datetime.timedelta(hours=9)
		else:
			ts_chat_url = 'https://api.twitch.tv/v5/videos/' + post_data['req_videoids'] + '/comments?cursor=' + post_data['req_next_token']
			# 2回目以降はrequestsから取得
			video_length=post_data['req_video_length']
			video_recorded_at_jst=dt.strptime(post_data['req_video_recorded_at_jst'],'%Y-%m-%d %H:%M:%S')

		# DBからts_chat_distを取得
		try:
			DB_data=DBModel.objects.get(md_name=post_data['req_videoids'])
			# print(DB_data)
			# DBから取得した直後は文字列なのでevalで辞書型リストに変換
			ts_chat_dist_old=eval(DB_data.md_ts_chat)
		# データが無い場合は空
		except:
			ts_chat_dist_old=[]

		# tsとchatを取得
		r = requests.get(ts_chat_url, headers=headers)
		ts_chat_data = r.json()
		# print(ts_chat_data)
		# print(json.dumps(ts_chat_data, indent=2))
		# tsとchatを辞書型リストに格納
		ts_chat_dist=[ {'timestamp(JST)':str(video_recorded_at_jst+datetime.timedelta(seconds=int(comment['content_offset_seconds']))), 'chat':comment['message']['body'] } for comment in ts_chat_data['comments'] ]
		# print(ts_chat_dist)

		# 進捗を計算
		# リストの最後のtsを取得
		last_ts=dt.strptime(ts_chat_dist[-1]['timestamp(JST)'],'%Y-%m-%d %H:%M:%S')-video_recorded_at_jst
		# print(last_ts,video_length)
		# 動画全体の時間から割合を取得して小数点以下切り捨て
		progress=math.floor(int(last_ts.seconds)/int(video_length)*100)
		# print(f'進捗：{progress}%')

		# DBに保存
		DBModel.objects.update_or_create(
			# ユニークな値
			md_name=post_data['req_videoids'],
			# 更新もしくは新規で追加したい値
			defaults={
				'md_ts_chat':ts_chat_dist_old+ts_chat_dist,
			}
		)

		json_resp={'videoids':post_data['req_videoids'],
		           'progress':progress,
		           'video_length':video_length,
		           'video_recorded_at_jst':str(video_recorded_at_jst),
		           }
		# next_tokenの有無でif
		if '_next' in ts_chat_data:
			json_resp['next_token']=ts_chat_data['_next']
		else:
			json_resp['next_token']='None'
		# print(json_resp)

	return JsonResponse(json_resp)
