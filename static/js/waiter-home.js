$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.passmsg = [];
    window.feedbackmsg = [];
    window.requestmsg = [];
    window.cleanmsg = [];
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
    $(document).on('tap', '.mask', function(){
	    window.location.replace('/waiter-mask');
    });
    $(document).on('tap', '.clean', function(){
	    window.location.replace('/waiter-clean');
    });
    $(document).on('tap', '.passwd', function(){
	    window.location.replace('/faculty-secret?back=waiter-home');
    });
    pass.poll();
    feedback.poll();
    request.poll();
    clean.poll();
});
function show_pass() {
    $('.pass .num').text(window.passmsg.length);
}
var pass = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    var desk = window.desk;
        console.log('polling', pass.cursor);
        pass.cursor += 1;
        pass.xhr = $.ajax({
            url: '/waiter-pass-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(pass.stamp)},
            success: pass.onSuccess,
            error: pass.onError
        });

    },
    onSuccess: function(response){
        window.passmsg = response.message;
        pass.stamp = response.stamp;
        show_pass();
        pass.interval = 800;
        setTimeout(pass.poll, pass.interval);
    },
    onError: function(response, error) {
        console.log(error);
        pass.interval = pass.interval*2;
        setTimeout(pass.poll, pass.interval);
    },
    reset: function(){
        pass.stamp = 0;
        pass.cursor = 0;
        pass.interval = 800;
        pass.xhr.abort();
    }
};
function show_feedback() {
    $('.feedback .num').text(window.feedbackmsg.length);
}
var feedback = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){

        console.log('polling', feedback.cursor);
        feedback.cursor += 1;
        feedback.xhr = $.ajax({
            url: '/waiter-feedback-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(feedback.stamp)},
            success: feedback.onSuccess,
            error: feedback.onError
        });

    },
    onSuccess: function(response){
        window.feedbackmsg = response.message;
        feedback.stamp = response.stamp;
        show_feedback();
        feedback.interval = 800;
        setTimeout(feedback.poll, feedback.interval);
    },
    onError: function(response, error) {
        console.log(error);
        feedback.interval = feedback.interval*2;
        setTimeout(feedback.poll, feedback.interval);
    },
    reset: function(){
        feedback.stamp = 0;
        feedback.cursor = 0;
        feedback.interval = 800;
        feedback.xhr.abort();
    }
};
function show_request(){
    $('.request .num').text(window.requestmsg.length);
}
var request = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){

        console.log('polling', request.cursor);
        request.cursor += 1;
        request.xhr = $.ajax({
            url: '/waiter-request-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(request.stamp)},
            success: request.onSuccess,
            error: request.onError
        });

    },
    onSuccess: function(response){
        window.requestmsg = response.message;
        request.stamp = response.stamp;
        show_request();
        request.interval = 800;
        setTimeout(request.poll, request.interval);
    },
    onError: function(response, error) {
        console.log(error);
        request.interval = request.interval*2;
        setTimeout(request.poll, request.interval);
    },
    reset: function(){
        request.stamp = 0;
        request.cursor = 0;
        request.interval = 800;
        request.xhr.abort();
    }
};
function show_clean(){
    $('.clean .num').text(window.cleanmsg.length);
}
var clean = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){

        console.log('polling', clean.cursor);
        clean.cursor += 1;
        clean.xhr = $.ajax({
            url: '/waiter-clean-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(clean.stamp)},
            success: clean.onSuccess,
            error: clean.onError
        });

    },
    onSuccess: function(response){
        window.cleanmsg = response.message;
        clean.stamp = response.stamp;
        show_clean();
        clean.interval = 800;
        setTimeout(clean.poll, clean.interval);
    },
    onError: function(response, error) {
        console.log(error);
        clean.interval = clean.interval*2;
        setTimeout(clean.poll, clean.interval);
    },
    reset: function(){
        clean.stamp = 0;
        clean.cursor = 0;
        clean.interval = 800;
        clean.xhr.abort();
    }
};
