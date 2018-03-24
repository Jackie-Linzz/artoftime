$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.desk = $('.heading').data('desk');
    window.message = [];

    $(document).on('click', '.back', function(){
	    window.location.replace('/');
    });
    $(document).on('click', '.order', function(){
	    window.location.replace('/customer-category?desk='+desk);
    });
    $(document).on('click', '.myorder', function(){
	    window.location.replace('/customer-order?desk='+desk);
    });
    $(document).on('click', '.fb', function(){
	    window.location.replace('/customer-feedback?desk='+desk);
    });
    $(document).on('click', '.call', function(){
	    $.postJSON(
	        '/customer-call',
	        {'desk': window.desk},
	        function(){}
	    );
    });
    $(document).on('click', '.qrcode', function(){
	    window.location.replace('/customer-home?desk='+desk);
    });
    updater.poll();
});

function show_message() {
    var flag = false;
    for(var i in window.message) {
	    if(window.desk == window.message[i]) {
	        flag = true;
	        break;
	    }
    }
    if(flag) {
	    $('.call').text('已呼叫').css('background-color', 'red');
    } else {
	    $('.call').text('呼叫服务员').css('background-color', '#376956');
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
            url: '/customer-request-update',
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
