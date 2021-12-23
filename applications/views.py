# from django.core import serializers
from django.shortcuts import render
from django.http import JsonResponse
from .models import BorderDataModel

def input_v1(request):
	TIME_DATA=['6:00～7:00',
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
	print(json_resp)
	base_data={'TIME_DATA':TIME_DATA,
						 'SHISETSU_DATA':SHISETSU_DATA,
						 'SHITUJOU_DATA':SHITUJOU_DATA,
						 'CORDER_DATA':CORDER_DATA,
						 'json_resp':json_resp}
	return render(request, 'applications/input_v1.html', base_data)

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