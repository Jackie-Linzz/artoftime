$(document).ready(function(){
    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.desks = [];
    window.queue = [];
    $(document).on('click', '.back', function(){
        window.location.replace('/waiter-home');
    });
    $(document).on('click', '.button', function(){
        var item = $(this).parents('.item');
        var order = item.data('order');
        $.postJSON(
            '/waiter-queue',
            {'order': order},
            function(response){}
        );
    });
    desk_updater.poll();
    queue_updater.poll();
});

function show_desks(){
    
    var p = $('.left').empty();
    if(window.desks.length == 0) return;
    for(var i in window.desks){
        var one = window.desks[i];
        var item = $('<div class="item"><span class="desk">1</span> (<span class="num">2</span>)</div>');
        item.find('.desk').text(one.desk);
        item.find('.num').text(one.num);
        p.append(item);
    }
}
function show_queue(){
    
    var p = $('.right').empty();
    if(window.queue.length == 0) return;
    for(var i in window.queue){
        var one = window.queue[i];
        var item = $('<div class="item"><span class="order">4</span> (<span class="num">2</span>)<div class="button">OK</div></div>');
        item.data('order', one.order);
        item.find('.order').text(one.order);
        item.find('.num').text(one.num);
        p.append(item);
    }
}
var desk_updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    
        console.log('polling', desk_updater.cursor);
        desk_updater.cursor += 1;
        desk_updater.xhr = $.ajax({
            url: '/waiter-desk-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(desk_updater.stamp)},
            success: desk_updater.onSuccess,
            error: desk_updater.onError
        });

    },
    onSuccess: function(response){
        //console.log(response);
        window.desks = response.desks;
        desk_updater.stamp = response.stamp;
        show_desks();
        desk_updater.interval = 800;
        setTimeout(desk_updater.poll, desk_updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        desk_updater.interval = desk_updater.interval*2;
        setTimeout(desk_updater.poll, desk_updater.interval);
    },
    reset: function(){
        desk_updater.stamp = 0;
        desk_updater.cursor = 0;
        desk_updater.interval = 800;
        desk_updater.xhr.abort();
    }
};
var queue_updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    
        console.log('polling', queue_updater.cursor);
        queue_updater.cursor += 1;
        queue_updater.xhr = $.ajax({
            url: '/waiter-queue-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(queue_updater.stamp)},
            success: queue_updater.onSuccess,
            error: queue_updater.onError
        });

    },
    onSuccess: function(response){
        //console.log(response);
        window.queue = response.queue;
        queue_updater.stamp = response.stamp;
        show_queue();
        queue_updater.interval = 800;
        setTimeout(queue_updater.poll, queue_updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        queue_updater.interval = queue_updater.interval*2;
        setTimeout(queue_updater.poll, queue_updater.interval);
    },
    reset: function(){
        queue_updater.stamp = 0;
        queue_updater.cursor = 0;
        queue_updater.interval = 800;
        queue_updater.xhr.abort();
    }
};
