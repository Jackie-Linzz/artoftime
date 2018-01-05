$(document).ready(function(){
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
