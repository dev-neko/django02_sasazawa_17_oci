from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import UserDataModel,BorderDataModel
from config.tasks import add,search_url,search_seller
from celery.result import AsyncResult



def input_v1(request):
	if request.user.is_authenticated:
		borderdata=BorderDataModel.objects.order_by("id").last()
		try:
			db_cancel_border=eval(borderdata.md_cancel_border)
		except:
			db_cancel_border=''
		try:
			db_reserve_border=eval(borderdata.md_reserve_border)
		except:
			db_reserve_border=''
		# 検索条件保存ボタンか検索条件呼び出しボタンが押されたときの処理
		if request.method=='POST':
			# 予約日時 保存 ボタン
			if request.POST["db_action_btn"]=="save":
				try:
					BorderDataModel.objects.update_or_create(md_name='border data',
																									 defaults={'md_reserve_border':request.POST["radio_reserve_border"]})
					borderdata=BorderDataModel.objects.order_by("id").last()
					db_reserve_border=eval(borderdata.md_reserve_border)
				except:
					BorderDataModel.objects.update_or_create(md_name='border data',
																									 defaults={'md_reserve_border':''})
					db_reserve_border=''
		dt_data={'db_cancel_border':db_cancel_border,
						 'db_reserve_border':db_reserve_border,
						 }
		return render(request, 'applications/input_v1.html', dt_data)
	else:
		return HttpResponseRedirect('/accounts/login/')


def userdata(request):
	if request.user.is_authenticated:
		try:
			userdata=UserDataModel.objects.get(md_name='user data')
			db_line_token=userdata.md_line_token
			db_to_email=userdata.md_to_email
			db_ac_id=userdata.md_ac_id
			db_ac_pass=userdata.md_ac_pass
		except:
			db_line_token=db_to_email=db_ac_id=db_ac_pass=''
		if request.method=='POST':
			UserDataModel.objects.update_or_create(md_name='user data',
																						 defaults={'md_line_token':request.POST['line_token'],
																											 'md_to_email':request.POST['to_email'],
																											 'md_ac_id':request.POST['ac_id'],
																											 'md_ac_pass':request.POST['ac_pass'],
																											 })
			userdata=UserDataModel.objects.get(md_name='user data')
			db_line_token=userdata.md_line_token
			db_to_email=userdata.md_to_email
			db_ac_id=userdata.md_ac_id
			db_ac_pass=userdata.md_ac_pass
		dt_data={'db_line_token':db_line_token,
						 'db_to_email':db_to_email,
						 'db_ac_id':db_ac_id,
						 'db_ac_pass':db_ac_pass,
						 }
		return render(request, 'registration/userdata.html',dt_data)
	else:
		return HttpResponseRedirect('/accounts/login/')