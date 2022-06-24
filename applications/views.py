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
		return HttpResponseRedirect('/accounts/login/')


# csvをzipでダウンロードするページの表示
def dl_csv_zip(request):
	# ログインの確認
	if request.user.is_authenticated:
		return render(request,'applications/dl_csv_zip.html')
	else:
		return HttpResponseRedirect('/accounts/login/')


# csvをzipでダウンロードする処理
def dl_csv_zip_proc(request):

	if request.method=='POST':

		# checkboxの内容をリストに格納
		checkbox_list=request.POST.getlist('checkbox')
		# actionがsaveかつ、checkbox_listが空でない場合
		# checkbox_listが空の場合に実行すると「zip」ファイルがダウンロードされてしまうのを防ぐ
		if request.POST.get('action')=='save' and checkbox_list:

			# csvに変換する内容
			csv_content={'1つ目':[{'ts': 4, 'chat': 'あああ'}, {'ts': 4, 'chat': 'いいい'}, {'ts': 5, 'chat': 'えええ'}],
			             '2つ目':[{'ts': 12, 'chat': 'aaa'}, {'ts': 22, 'chat': 'おおお'}, {'ts': 50, 'chat': 'bbb'}],
			             '3つ目':[{'ts': 0, 'chat': 'ccc'}, {'ts': 11, 'chat': 'ををを'}, {'ts': 19, 'chat': 'ddd'}]
			             }

			# 書き込むzipの準備
			memory_file=BytesIO() #エラーなし
			# res_zip=StringIO() #TypeError string argument expected, got 'bytes'
			# res_zip = HttpResponse(content_type='application/zip') #予期しない型
			zip_file=zipfile.ZipFile(memory_file,'w')

			# key='1つ目' value=[{'ts': 4, 'chat': 'あああ'}, {'ts': 4, 'chat': 'いいい'}, {'ts': 5, 'chat': 'えええ'}]
			# key='2つ目' value=[{'ts': 12, 'chat': 'aaa'}, {'ts': 22, 'chat': 'おおお'}, {'ts': 50, 'chat': 'bbb'}]
			# key='3つ目' value=[{'ts': 0, 'chat': 'ccc'}, {'ts': 11, 'chat': 'ををを'}, {'ts': 19, 'chat': 'ddd'}]
			# 上記の順番でkey,valueに格納してfor
			for key,value in csv_content.items():
				# keyがチェックした要素に含まれている場合
				if key in checkbox_list:
					# csvの準備
					csv_file=HttpResponse(content_type='text/csv')
					# csv_file=BytesIO() #TypeError: a bytes-like object is required, not 'str'
					# csvへヘッダーの書き込み
					writer=csv.DictWriter(csv_file,['ts','chat'])
					writer.writeheader()
					# csvへの書き込み
					writer.writerows(value)
					# zipに圧縮
					zip_file.writestr(f'{key}.csv',csv_file.getvalue())
					csv_file.close()

			# zipの内容をreponseに設定
			zip_file.close() #ここでcloseしないとエラーが発生して解凍できない
			response=HttpResponse(memory_file.getvalue(), content_type='application/zip')
			# checkbox_listを,で区切ってURLエンコード
			quoted_filename = urllib.parse.quote(",".join(checkbox_list))
			# quoted_filenameをファイル名にする
			# filename*にURLエンコードしたファイル名をセットすることで日本語のファイル名にも対応可能
			response['Content-Disposition']=f'attachment; filename="{quoted_filename}.zip"; filename*=UTF-8"{quoted_filename}.zip"'

			# responseを返す
			return response

		# checkbox_listが空の場合は何もしないのでstatus=204を返す
		else:
			return HttpResponse(status=204)