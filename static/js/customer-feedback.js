$(document).ready(function(){
    window.fb = [];
    var desk = $('.heading').attr('data-desk');
    $(document).on('tap', '.left', function(){
	window.location.replace('/customer-home?desk='+desk);
    });
    $(document).on('tap', '.item .fb', function(){
	var item = $(this).parents('.item');
	item.find('.fb').removeClass('selected');
	$(this).addClass('selected');
    });
    $(document).on('tap', '.footer', function(){
	var comment = $('.comment').val();
	comment = trim(comment);
	fb = [];
	$('.selected').each(function(){
	    var item = $(this).parents('.item');
	    var uid = item.attr('data-uid');
	    var f = $(this).attr('data-fb');
	    fb.push({'uid': uid, 'fb': Number(f)});
	});
	$.postJSON(
	    '/customer-feedback',
	    {'desk': desk, 'comment': json(comment), 'fb': json(fb)},
	    function(){}
	);
    });
});
