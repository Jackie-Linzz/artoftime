$(document).ready(function(){
    $('.tab').hide();
    
    $(document).on('tap', '#select', function(){
	$('.tab').hide();
	$('.select').show();
    });
    $(document).on('tap', '#doing', function(){
	$('.tab').hide();
	$('.doing').show();
    });
    $(document).on('tap', '#done', function(){
	$('.tab').hide();
	$('.done').show();
    });
    $(document).on('tap', '.back', function(){
	window.location.replace('/cook-home');
    });
    $(document).on('tap', '.byway .item', function(){
	$(this).toggleClass('selected');
    });
});
