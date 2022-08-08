import csv
import math
import time
import urllib.parse
import zipfile
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse


# リンクページの表示
def index(request):
	# ログインの確認
	if request.user.is_authenticated:
		return render(request,'applications/index.html')
	else:
		# ログインしていない場合はログインページへ移動
		return HttpResponseRedirect('/accounts/login/')


# csvをzipでダウンロードするページの表示
def dl_csv_zip(request):
	# ログインの確認
	if request.user.is_authenticated:
		return render(request,'applications/dl_csv_zip.html')
	else:
		# ログインしていない場合はログインページへ移動
		return HttpResponseRedirect('/accounts/login/')


# 指定された辞書型リストをcsvに変換してzipでダウンロードする処理
def dl_csv_zip_proc(request):

	if request.method=='POST':
		# postされたcheckboxの内容をリストに格納
		checkbox_list=request.POST.getlist('checkbox')
		# actionがsaveかつ、checkbox_listが空でない場合
		# checkbox_listが空の場合に実行すると「zip」ファイルがダウンロードされてしまうのを防ぐ
		if request.POST.get('action')=='save' and checkbox_list:

			# 書き込むzipの準備
			memory_file=BytesIO()
			zip_file=zipfile.ZipFile(memory_file,'w')

			for item in checkbox_list:
				# csvの準備
				csv_file=HttpResponse(content_type='text/csv')
				# csvヘッダーの書き込み
				writer=csv.DictWriter(csv_file,['ts','chat'])
				writer.writeheader()
				# csvへの書き込み
				# postされたtextareaの内容は文字列のためevalで辞書型リストに変換
				writer.writerows(eval(request.POST.get(item)))
				# zipに圧縮
				zip_file.writestr(f'{item}.csv',csv_file.getvalue())
				csv_file.close()

			# zipの内容をreponseに設定
			#ここでcloseしないとエラーが発生して解凍できない
			zip_file.close()
			response=HttpResponse(memory_file.getvalue(), content_type='application/zip')
			# checkbox_listを「,」で区切ってURLエンコード
			quoted_filename = urllib.parse.quote(",".join(checkbox_list))
			# quoted_filenameをファイル名にする
			# filename*にURLエンコードしたファイル名をセットすることで日本語のファイル名にも対応可能
			response['Content-Disposition']=f'attachment; filename="{quoted_filename}.zip"; filename*=UTF-8"{quoted_filename}.zip"'

			# responseを返す
			return response

		# checkbox_listが空の場合は何もしないのでstatus=204を返す
		else:
			return HttpResponse(status=204)


# rec_ajaxページの表示
def rec_ajax(request):
	# ログインの確認
	if request.user.is_authenticated:
		return render(request,'applications/rec_ajax.html')
	else:
		# ログインしていない場合はログインページへ移動
		return HttpResponseRedirect('/accounts/login/')


# rec_ajaxの処理
def rec_ajax_proc(request):

	if request.method=='POST':
		# 進捗を計算するためにint型に変換
		select_num=int(request.POST.get('select_num'))

		# 1回目はnext_numがないため、tryで処理を分ける
		try:
			# postデータから取得し、進捗を計算するためにint型に変換
			current_num=int(request.POST.get('next_num'))
		except:
			# postデータからは取得できないため初期値を定義する
			current_num=1

		print(f'select_num：{select_num}')
		print(f'current_num：{current_num}')

		# 進捗(%)を計算
		# select_numから割合を算出してmath.floorで小数点以下切り捨て
		progress=math.floor(current_num/select_num*100)
		print(f'進捗：{progress}%')

		# ajaxに返すjsonレスポンス
		json_resp={'select_num':select_num, # formで選択した数値
		           'current_num':current_num, # 現在値
		           'next_num':current_num+1, # 次の数値
		           'progress':progress, # 進捗(%)
		           }

		# formで選択した数値と現在値を比較して、json_resp辞書にkey→'state'、value→状態を追加
		if select_num==current_num:
			json_resp['state']='終了'
		else:
			json_resp['state']='実行中'

		print(f'json_resp：{json_resp}')

		# 処理はほぼ一瞬で終了してしまうためスリープ
		time.sleep(1)

	return JsonResponse(json_resp)


# help_modalページの表示
def help_modal(request):
	# ログインの確認
	if request.user.is_authenticated:
		return render(request,'applications/help_modal.html')
	else:
		# ログインしていない場合はログインページへ移動
		return HttpResponseRedirect('/accounts/login/')
