$(document).ready(function(){
    $(document).on('tap', '.back', function(){
	window.location.replace('/faculty-role');
    });
    $(document).on('tap', '.order', function(){
	window.location.replace('/waiter-order');
    });
    $(document).on('tap', '.pass', function(){
	window.location.replace('/waiter-pass');
    });
    $(document).on('tap', '.feedback', function(){
	window.location.replace('/waiter-feedback');
    });
    $(document).on('tap', '.request', function(){
	window.location.replace('/waiter-request');
    });
    $(document).on('tap', '.clean', function(){
	window.location.replace('/waiter-clean');
    });
    $(document).on('tap', '.passwd', function(){
	window.location.replace('/faculty-secret');
    });
});
