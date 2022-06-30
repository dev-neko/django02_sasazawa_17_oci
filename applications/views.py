import csv
import urllib.parse
import zipfile
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse


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