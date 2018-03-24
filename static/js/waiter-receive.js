$(document).ready(function(){
    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.left = [];
    window.done = [];

    $('.left-content').show();
    $('.done-content').hide();

    $(document).on('click', '.back', function(){
        window.location.replace('/waiter-home');
    });
    $(document).on('click', '.left', function(){
        $('.left-content').show();
        $('.done-content').hide();
    });
    $(document).on('click', '.done', function(){
        $('.left-content').hide();
        $('.done-content').show();
    });
    $(document).on('click', '.item .button', function(){
        var item = $(this).parents('.item');
        var uid = item.data('uid');
        $.postJSON(
            '/waiter-done',
            {'uid': uid},
            function(){}
        );
    });
    left_updater.poll();
    done_updater.poll();
});

function show_left() {
    var p = $('.left-content').empty();
    if(window.left.length == 0) return;
    
    for(var i in window.left) {
        var one = window.left[i];
        var item = $('<div class="item"><div class="msg"></div><div class="button">OK</div></div>');
        item.data('uid', one.uid);
        item.find('.msg').text(one.desk+':'+one.name+":"+one.num);
        p.append(item);
    }
}

function show_done(){
    var p = $('.done-content').empty();
    if(window.done.length == 0) return;
    
    for(var i in window.done) {
        var one = window.done[i];
        var item = $('<div class="item"><div class="msg"></div></div>');
        item.data('uid', one.uid);
        item.find('.msg').text(one.desk+':'+one.name+":"+one.num);
        p.append(item);
    }
}

var left_updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    
        console.log('polling', left_updater.cursor);
        left_updater.cursor += 1;
        left_updater.xhr = $.ajax({
            url: '/waiter-left-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(left_updater.stamp)},
            success: left_updater.onSuccess,
            error: left_updater.onError
        });

    },
    onSuccess: function(response){
        //console.log(response);
        window.left = response.left;
        left_updater.stamp = response.stamp;
        show_left();
        left_updater.interval = 800;
        setTimeout(left_updater.poll, left_updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        left_updater.interval = left_updater.interval*2;
        setTimeout(left_updater.poll, left_updater.interval);
    },
    reset: function(){
        left_updater.stamp = 0;
        left_updater.cursor = 0;
        left_updater.interval = 800;
        left_updater.xhr.abort();
    }
};

var done_updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    
        console.log('polling', done_updater.cursor);
        done_updater.cursor += 1;
        done_updater.xhr = $.ajax({
            url: '/waiter-done-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(done_updater.stamp)},
            success: done_updater.onSuccess,
            error: done_updater.onError
        });

    },
    onSuccess: function(response){
        //console.log(response);
        window.done = response.done.done;
        done_updater.stamp = response.stamp;
        show_done();
        done_updater.interval = 800;
        setTimeout(done_updater.poll, done_updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        done_updater.interval = done_updater.interval*2;
        setTimeout(done_updater.poll, done_updater.interval);
    },
    reset: function(){
        done_updater.stamp = 0;
        done_updater.cursor = 0;
        done_updater.interval = 800;
        done_updater.xhr.abort();
    }
};


