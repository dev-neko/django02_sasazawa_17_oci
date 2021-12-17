from django.core import serializers
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
	# ページ読み込み時にDBのデータを読み込む
	# jsonに変換してもただの文字列の様なのでevalしてそこから取り出す
	try:
		borderdata=eval(serializers.serialize('json',BorderDataModel.objects.all()))
		json_resp=borderdata[0]["fields"]
	except:
		json_resp={}
	base_data={'TIME_DATA':TIME_DATA,
						 'SHISETSU_DATA':SHISETSU_DATA,
						 'SHITUJOU_DATA':SHITUJOU_DATA,
						 'json_resp':json_resp}
	return render(request, 'applications/input_v1.html', base_data)

def ajax_proc(request):
	if request.method=='POST':
		# print(request.POST)
		# 保存ボタン
		if request.POST["db_action"]=="save":
			BorderDataModel.objects.update_or_create(
				md_name='border data',
				defaults={'md_r_day':request.POST.get('r_day'),
									'md_r_time':request.POST.get('r_time'),
									'md_r_shisetsu':request.POST.get('r_shisetsu'),
									'md_r_shitsujou':request.POST.get('r_shitsujou')})
			# jsonに変換してもただの文字列の様なのでevalしてそこから取り出す
			borderdata=eval(serializers.serialize('json',BorderDataModel.objects.all()))
			json_resp=borderdata[0]["fields"]
			print(f'予約日を登録した：{json_resp}')
		# 削除ボタン
		elif request.POST["db_action"]=="delete":
			BorderDataModel.objects.all().delete()
			json_resp={}
			print(f'予約日を削除した：{json_resp}')
	return JsonResponse(json_resp)