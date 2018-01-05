$(document).ready(function(){
    $('.content').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/manager-home');
    });
    $(document).on('tap', '.menu .op', function(){
	$('.content').show();
	$('.comment').remove();
	var more = $('.more');
	$.postJSON(
	    '/manager-comment-show',
	    {},
	    function(response) {
		if(response.status != 'ok') return;
		var comments = response.comments;
		for(var i in comments) {
		    var one = comments[i];
		    var div = $('<div class="comment">'+
				'<div class="message">liuyan</div>'+
				'<div class="stamp">2017-12-31</div>'+
				'</div>');
		    div.find('.message').text(one.comment);
		    div.find('.stamp').text(one.stamp);
		    more.before(div);
		}
	    }
	);
    });
    $(document).on('tap', '.more', function(){
	var more = $('.more');
	$.postJSON(
	    '/manager-comment-more',
	    {},
	    function(response) {
		if(response.status != 'ok') return;
		var comments = response.comments;
		for(var i in comments) {
		    var one = comments[i];
		    var div = $('<div class="comment">'+
				'<div class="message">liuyan</div>'+
				'<div class="stamp">2017-12-31</div>'+
				'</div>');
		    div.find('.message').text(one.comment);
		    div.find('.stamp').text(one.stamp);
		    more.before(div);
		}
	    }
	);
    });
});
