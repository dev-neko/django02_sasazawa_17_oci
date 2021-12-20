// ----- Ajax前のおまじない start -----
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
// ----- Ajax前のおまじない end -----

// スライダーの操作を検知する
// inputにするとリアルタイムで検知が可能
$('#ajax_form').on('submit', function(e) { //---(1)
	// フォームでスライダーが操作されたときに、フォーム送信の通信を止めるためにpreventDefault()を使用
	e.preventDefault();
	// サーバに送信するリクエストの設定
	$.ajax({
		// リクエストを送信するURLを指定
		// propメソッドを用いればformの内容を引き継げるのでjsを外部に設置可能
		'url': $('#ajax_form').prop("action"), //---(1)
		// HTTPメソッドのGET通信かPOST通信を指定
		'method': $('#ajax_form').prop("method"),
		// サーバに送信するデータの指定
		'data': {
			'r_day':$('#r_day').val(),
			'r_time':$('#r_time').val(),
			'r_shisetsu':$('#r_shisetsu').val(),
			'r_shitsujou':$('#r_shitsujou').val(),
			'r_corder':$('#r_corder').val(),
			'db_action':$('#db_action').val(),
		},
		// データ形式(ここではjson)を指定
		'dataType': 'json'
	})
	// 通信成功時の処理
	// views.pyから受け取ったJSONデータをページに表示
	.done(function(response){
		// 内容を初期化
		$('.result').empty();
		// responseが空でなければ
		if (!(jQuery.isEmptyObject(response))) {
			// 登録時のtoast表示
			$("#toast_save").toast({delay:3000}).toast('show');
			// append だと後ろに追加、prependは前に追加
			$('.result').append('<p>日付：' + response.md_r_day + '</p>');
			$('.result').append('<p>時間：' + response.md_r_time + '</p>');
			$('.result').append('<p>施設名：' + response.md_r_shisetsu + '</p>');
			$('.result').append('<p>室場名：' + response.md_r_shitsujou + '</p>');
			$('.result').append('<p>コート番号：' + response.md_r_corder + '</p>');
		} else {
			// 削除時のtoast表示
			$("#toast_delete").toast({delay:3000}).toast('show');
		}
	})
	// 通信失敗時の処理
	.fail(function(){
		window.alert("error");
	});
});

// form内のinput hiddenの内容をボタンごとに書き換えてsubmitすることでボタンによって処理を分ける
// https://technote925.com/106
$(function(){
	$('#save_btn').click(function() {
		$('#db_action').attr('value', 'save');
		$('#ajax_form').submit();
	});
	$('#delete_btn').click(function() {
		$('#db_action').attr('value', 'delete');
		$('#ajax_form').submit();
	});
});

