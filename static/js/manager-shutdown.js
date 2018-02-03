$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	var css = $('#css').attr('href');
	css = css.replace(/-mobile/g, '');
	$('#css').attr('href', css);
    }
    $('.shutdown').hide();
    $('.reboot').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/manager-home');
    });
    $(document).on('tap', '.op-shutdown', function(){
	$('.shutdown').show();
	$('.reboot').hide();
    });
    $(document).on('tap', '.op-reboot', function(){
	$('.shutdown').hide();
	$('.reboot').show();
    });
    $(document).on('tap', '.shutdown .button', function(){
	$.postJSON(
	    '/manager-shutdown',
	    {},
	    function(){}
	);
    });
    $(document).on('tap', '.reboot .button', function(){
	$.postJSON(
	    '/manager-reboot',
	    {},
	    function(){}
	);
    });
});
