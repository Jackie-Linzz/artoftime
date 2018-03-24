$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.fb = [];
    window.desk = $('.heading').attr('data-desk');

    $.postJSON(
	    '/customer-comment',
	    {'desk': window.desk},
	    function(response) {
	        if(response.status != 'ok') return;
	        $('.comment').val(response.comment);
	    }
    );

    $(document).on('click', '.left', function(){
	    window.location.replace('/customer-home?desk='+desk);
    });
    $(document).on('click', '.item .fb', function(){
	    var item = $(this).parents('.item');
	    item.find('.fb').removeClass('selected');
	    $(this).addClass('selected');
    });
    $(document).on('click', '.footer', function(){
	    var comment = $('.comment').val();
	    comment = trim(comment);
	    fb = [];
	    $('.selected').each(function(){
	        var item = $(this).parents('.item');
	        var uid = item.attr('data-uid');
	        var f = $(this).attr('data-fb');
	        fb.push({'uid': Number(uid), 'fb': Number(f)});
	    });
	    console.log(fb);
	    $.postJSON(
	        '/customer-feedback',
	        {'desk': desk, 'comment': json(comment), 'fb': json(fb)},
	        function(response){
		        if(response.status != 'ok') return;
		        $('.selected').parents('.item').remove();
	        }
	    );
    });
});
