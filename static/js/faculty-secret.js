$(document).ready(function(){
    var back = $('body').data('back');
    $('.msg').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/'+back);
    });
    $(document).on('tap', '.button', function(){
	var p1 = trim($('#passwd1').val());
	var p2 = trim($('#passwd2').val());
	var p3 = trim($('#passwd3').val());
	$('.msg').hide();

	if(p1==''||p2==''||p3=='') {
	    $('.msg').text('密码不能为空');
	    $('.msg').show();
	    return;
	}
	if(p2 != p3) {
	    $('.msg').text('新密码不一致');
	    $('.msg').show();
	    return;
	}
	$.postJSON(
	    '/faculty-secret',
	    {'passwd1': p1, 'passwd2': p2, 'passwd3': p3},
	    function(response) {
		if(response.status == 'failure') {
		    $('.msg').text('更新失败');
		    $('.msg').show();
		    return;
		}
		if(response.status == 'success') {
		    $('.msg').text('更新成功');
		    $('.msg').show();
		    return;
		}
	    }
	);
    });
});
