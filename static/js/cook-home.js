$(document).ready(function(){
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
