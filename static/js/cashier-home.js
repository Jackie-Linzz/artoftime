$(document).ready(function(){
    $(document).on('tap', '.back', function(){
	window.location.replace('/faculty-role');
    });
    $(document).on('tap', '.work', function(){
	window.location.replace('/cashier-work');
    });
    $(document).on('tap', '.passwd', function(){
	window.location.replace('/faculty-secret?back=cashier-home');
    });
});
