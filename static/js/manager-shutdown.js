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
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '.op-shutdown', function(){
	    $('.shutdown').show();
	    $('.reboot').hide();
    });
    $(document).on('click', '.op-reboot', function(){
	    $('.shutdown').hide();
	    $('.reboot').show();
    });
    $(document).on('click', '.shutdown .button', function(){
	    $.postJSON(
	        '/manager-shutdown',
	        {},
	        function(){}
	    );
    });
    $(document).on('click', '.reboot .button', function(){
	    $.postJSON(
	        '/manager-reboot',
	        {},
	        function(){}
	    );
    });
});
