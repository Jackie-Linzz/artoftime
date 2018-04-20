$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.receive = 0;
    window.pass = 0;
    window.feedback = 0;
    window.request = 0;
    window.clean = 0;
    $(document).on('click', '.back', function(){
	    window.location.replace('/faculty-role');
    });
    $(document).on('click', '.order', function(){
	    window.location.replace('/waiter-order');
    });
    $(document).on('click', '.receive', function(){
        window.location.replace('/waiter-receive');
    });
    $(document).on('click', '.pass', function(){
	    window.location.replace('/waiter-pass');
    });
    $(document).on('click', '.feedback', function(){
	    window.location.replace('/waiter-feedback');
    });
    $(document).on('click', '.request', function(){
	    window.location.replace('/waiter-request');
    });
    $(document).on('click', '.mask', function(){
	    window.location.replace('/waiter-mask');
    });
    $(document).on('click', '.clean', function(){
	    window.location.replace('/waiter-clean');
    });
    $(document).on('click', '.query', function(){
        window.location.replace('/waiter-query');
    });
    $(document).on('click', '.queue', function(){
        window.location.replace('/waiter-queue');
    });
    $(document).on('click', '.passwd', function(){
	    window.location.replace('/faculty-secret?back=waiter-home');
    });
    updater.poll();
});
function show() {
    $('.receive .num').text(window.receive);
    $('.pass .num').text(window.pass);
    $('.feedback .num').text(window.feedback);
    $('.request .num').text(window.request);
    $('.clean .num').text(window.clean);
}
var updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    var desk = window.desk;
        console.log('polling', updater.cursor);
        updater.cursor += 1;
        updater.xhr = $.ajax({
            url: '/waiter-status-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(updater.stamp)},
            success: updater.onSuccess,
            error: updater.onError
        });

    },
    onSuccess: function(response){
        window.receive = response.message.receive;
        window.pass = response.message.pass;
        window.feedback = response.message.feedback;
        window.request = response.message.request;
        window.clean = response.message.clean;
        updater.stamp = response.stamp;
        show();
        updater.interval = 800;
        setTimeout(updater.poll, updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        updater.interval = updater.interval * 2;
        setTimeout(updater.poll, updater.interval);
    },
    reset: function(){
        updater.stamp = 0;
        updater.cursor = 0;
        updater.interval = 800;
        updater.xhr.abort();
    }
};
