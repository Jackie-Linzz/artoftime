$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $('.content').hide();
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '.menu .op', function(){
	    $('.content').show();
	    $('.comment').remove();
	    var more = $('.more');
	    $.postJSON(
	        '/manager-comment-show',
	        {},
	        function(response) {
		        if(response.status != 'ok') return;
		        var comments = response.comments;
		        console.log(comments);
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
    $(document).on('click', '.more', function(){
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
