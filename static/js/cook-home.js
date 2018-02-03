$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	var css = $('#css').attr('href');
	css = css.replace(/-mobile/g, '');
	$('#css').attr('href', css);
    }
    $(document).on('tap', '.back', function(){
	window.location.replace('/faculty-role');
    });
    $(document).on('tap', '.work', function(){
	window.location.replace('/cook-work');
    });
    $(document).on('tap', '.cookdo', function(){
	window.location.replace('/cook-do');
    });
    $(document).on('tap', '.passwd', function(){
	window.location.replace('/faculty-secret?back=cook-home');
    });
});
