$(document).ready(function(){
    $(document).on('tap', '.back', function(){
	window.location.replace('/faculty-role');
    });
    $(document).on('tap', '.company', function(){
	window.location.replace('/manager-company');
    });
    $(document).on('tap', '.diet', function(){
	window.location.replace('/manager-diet');
    });
    $(document).on('tap', '.desk', function(){
	window.location.replace('/manager-desk');
    });
    $(document).on('tap', '.faculty', function(){
	window.location.replace('/manager-worker');
    });
    $(document).on('tap', '.cookdo', function(){
	window.location.replace('/manager-cookdo');
    });
    $(document).on('tap', '.achievement', function(){
	window.location.replace('/manager-achievement');
    });
    $(document).on('tap', '.flow', function(){
	window.location.replace('/manager-history');
    });
    $(document).on('tap', '.comment', function(){
	window.location.replace('/manager-comment');
    });
    $(document).on('tap', '.mask', function(){
	window.location.replace('/manager-mask');
    });
    $(document).on('tap', '.passwd', function(){
	window.location.replace('/faculty-secret?back=manager-home');
    });
    $(document).on('tap', '.shutdown', function(){
	window.location.replace('/manager-shutdown');
    });
});
