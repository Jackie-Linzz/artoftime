$(document).ready(function(){
    var desk = $('.heading').attr('data-desk');
    $(document).on('tap', '.order', function(){
	window.location.replace('/customer-category?desk='+desk);
    });
    $(document).on('tap', '.myorder', function(){
	window.location.replace('/customer-order?desk='+desk);
    });
    $(document).on('tap', '.fb', function(){
	window.location.replace('/customer-feedback?desk='+desk);
    });
    $(document).on('tap', '.call', function(){
	
    });
});
