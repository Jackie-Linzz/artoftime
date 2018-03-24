$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.message = [];
    $('.back').on('click', function(){
	    window.location.replace('/waiter-home');
    });
    $(document).on('click', '.item .button', function(){
	    var desk = $(this).parents('.item').data('desk');
	    $.postJSON(
	        '/waiter-feedback-remove',
	        {'desk': desk},
	        function(response){}
	    );
    });
    updater.poll();
});

function show_message() {
    var p = $('.content').empty();
    for(var i in window.message) {
	    var one = window.message[i];
	    var item = $('<div class="item"><div class="msg">desk</div><div class="button">确定</div></div>');
	    item.data('desk', one);
	    item.find('.msg').text(one);
	    p.append(item);
    }
}
var updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){

        console.log('polling', updater.cursor);
        updater.cursor += 1;
        updater.xhr = $.ajax({
            url: '/waiter-feedback-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(updater.stamp)},
            success: updater.onSuccess,
            error: updater.onError
        });

    },
    onSuccess: function(response){
        window.message = response.message;
        updater.stamp = response.stamp;
        show_message();
        updater.interval = 800;
        setTimeout(updater.poll, updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        updater.interval = updater.interval*2;
        setTimeout(updater.poll, updater.interval);
    },
    reset: function(){
        updater.stamp = 0;
        updater.cursor = 0;
        updater.interval = 800;
        updater.xhr.abort();
    }
};
