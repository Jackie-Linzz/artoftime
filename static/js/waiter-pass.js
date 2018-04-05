$(document).ready(function(){
    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.pass = [];
    window.passed = []
    $('.pass-content').show();
    $('.passed-content').hide();
    $('.back').on('click', function(){
	    window.location.replace('/waiter-home');
    });
    $(document).on('click', '.pass', function(){
        $('.pass-content').show();
        $('.passed-content').hide();
    });
    $(document).on('click', '.passed', function(){
        $('.pass-content').hide();
        $('.passed-content').show();
    });
    $(document).on('click', '.pass-content .item .button', function(e){
        //console.log(e);
	    var uid = $(this).parents('.item').data('uid');
	    $.postJSON(
	        '/waiter-pass-remove',
	        {'uid': uid},
	        function(response){
                
            }
	    );
    });
    pass_updater.poll();
    passed_updater.poll();
});

function show_pass() {
    var p = $('.pass-content').empty();
    for(var i in window.pass) {
	    var one = window.pass[i];
	    var item = $('<div class="item"><div class="msg">diet:desk:cook</div><div class="button">确定</div></div>');
	    item.data(one);
	    item.find('.msg').text(one.name+':'+one.demand+','+one.gdemand+':'+one.desk+':'+one.cookname);
	    p.append(item);
    }
}
function show_passed() {
    var p = $('.passed-content').empty();
    for(var i in window.passed) {
	    var one = window.passed[i];
	    var item = $('<div class="item"><div class="msg">diet:desk:cook</div></div>');
	    item.data(one);
	    item.find('.msg').text(one.name+':'+one.demand+','+one.gdemand+':'+one.desk+':'+one.cookname);
	    p.append(item);
    }
}

var pass_updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    var desk = window.desk;
        console.log('polling', pass_updater.cursor);
        pass_updater.cursor += 1;
        pass_updater.xhr = $.ajax({
            url: '/waiter-pass-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(pass_updater.stamp)},
            success: pass_updater.onSuccess,
            error: pass_updater.onError
        });

    },
    onSuccess: function(response){
        //console.log(response);
        window.pass = response.message;
        pass_updater.stamp = response.stamp;
        show_pass();
        pass_updater.interval = 800;
        setTimeout(pass_updater.poll, pass_updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        pass_updater.interval = pass_updater.interval*2;
        setTimeout(pass_updater.poll, pass_updater.interval);
    },
    reset: function(){
        pass_updater.stamp = 0;
        pass_updater.cursor = 0;
        pass_updater.interval = 800;
        pass_updater.xhr.abort();
    }
};
var passed_updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    var desk = window.desk;
        console.log('polling', passed_updater.cursor);
        passed_updater.cursor += 1;
        passed_updater.xhr = $.ajax({
            url: '/waiter-done-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(passed_updater.stamp)},
            success: passed_updater.onSuccess,
            error: passed_updater.onError
        });

    },
    onSuccess: function(response){
        //console.log(response);
        window.passed = response.done.passed;
        passed_updater.stamp = response.stamp;
        show_passed();
        passed_updater.interval = 800;
        setTimeout(passed_updater.poll, passed_updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        passed_updater.interval = passed_updater.interval*2;
        setTimeout(passed_updater.poll, passed_updater.interval);
    },
    reset: function(){
        passed_updater.stamp = 0;
        passed_updater.cursor = 0;
        passed_updater.interval = 800;
        passed_updater.xhr.abort();
    }
};
