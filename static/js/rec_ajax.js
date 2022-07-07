// ------------------------------
// Ajax前のおまじない start
// ------------------------------
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
	beforeSend: function (xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	}
});
// ------------------------------
// Ajax前のおまじない end
// ------------------------------


// --------------------------------
// ajax_form用のajax処理 start
// --------------------------------
// ajax_formでの操作を検知し、submitボタンが押され次第処理を行う
$('#ajax_form').on('submit', function(e) {
	// フォーム送信の通信を止めるためにpreventDefault()を使用
	e.preventDefault();
	// 2度押しを防止するため実行中はボタンを無効化する
	$("#run_btn").prop("disabled",true).text('実行中…');
	// サーバーに送信するリクエストの設定
	$.ajax({
		// リクエストを送信するURLを指定
		// propメソッドを用いればformの内容を引き継げるのでjsを外部に設置可能
		'url': $('#ajax_form').prop("action"),
		// HTTPメソッドのGET通信かPOST通信を指定
		'method': $('#ajax_form').prop("method"),
		// views.pyに送信するデータの指定
		'data': {
			// ajax.htmlのid="select_num"を指定し、セレクトボックスで選択されている表示文字列を取り出す
			'select_num':$('#select_num option:selected').text(),
		},
		// データ形式にjsonを指定
		'dataType': 'json'
	})
	// 通信成功時の処理
	.done(function(response){
		// ボタンにスピナーを追加
		$('#run_btn').replaceWith('<button onFocus="this.blur()" type="submit" class="btn btn-primary" id="run_btn" disabled><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 実行中…</button>');
		// views.pyから受け取ったjsonデータでテーブルを更新
		// 現在値
		$('#current_num_cell').replaceWith('<td id="current_num_cell">'+response.current_num+'</td>');
		// 状態
		$('#state_cell').replaceWith('<td id="state_cell">'+response.state+'</td>');
		// 進捗
		$('#progress_cell').replaceWith('<td id="progress_cell"><div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" style="width:'+response.progress+'%" role="progressbar" aria-valuenow="'+response.progress+'" aria-valuemin="0" aria-valuemax="100">'+response.progress+'%</div></div></td>');
		// ajax処理を行う再帰関数に引数を渡して呼び出す
		after_ajax(response.select_num,response.next_num);
	})
	// 通信失敗時の処理
	.fail(function(){
		window.alert("error");
	});
});
// --------------------------------
// ajax_form用のajax処理 end
// --------------------------------


// --------------------------------
// ajax処理を行う再帰関数 start
// --------------------------------
// 重複するコメントは省略
function after_ajax(select_num,next_num){
	$.ajax({
		'url':$('#ajax_form').prop("action"),
		'method':$('#ajax_form').prop("method"),
		// 引数をそのままviews.pyに送信する
		'data':{
			'select_num':select_num,
			'next_num':next_num,
		},
		'dataType':'json'
	})
	.done(function(response){
		$('#current_num_cell').replaceWith('<td id="current_num_cell">'+response.current_num+'</td>');
		$('#state_cell').replaceWith('<td id="state_cell">'+response.state+'</td>');
		$('#progress_cell').replaceWith('<td id="progress_cell"><div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" style="width:'+response.progress+'%" role="progressbar" aria-valuenow="'+response.progress+'" aria-valuemin="0" aria-valuemax="100">'+response.progress+'%</div></div></td>');
		// response.stateが「実行中」であれば同様の引数を渡して再帰呼び出し
		if (response.state == '実行中') {
			after_ajax(response.select_num,response.next_num);
		// response.stateが「終了」であれば1秒待機後ページをリロード
		} else if (response.state == '終了') {
			setTimeout(function(){location.reload()},1000);
		}
	})
	.fail(function(){
		window.alert("error");
	});
}
// --------------------------------
// ajax処理を行う再帰関数 end
// --------------------------------