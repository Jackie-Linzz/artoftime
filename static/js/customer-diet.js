$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    var desk = $('.heading').attr('data-desk');
    var cid = $('.heading').attr('data-cid');
    $(document).on('click', '.left', function(){
	    window.location.replace('/customer-category?desk='+desk);
    });
    $(document).on('click', '.detail', function(){
	    var did = $(this).parents('.item').attr('data-did');
	    window.location.replace('/customer-detail?desk='+desk+'&did='+did);
    });
    $(document).on('click', '.button', function(){
	    $(this).removeClass('animation');
	    $(this).addClass('animation');
	    //$(this).removeClass('animation');
	    //setTimeout("$(this).removeClass('animation')", 1500);
	    var did = $(this).parents('.item').attr('data-did');
	    var ins = ['+', did, ''];
	    $.postJSON(
	        '/customer-ins',
	        {'desk': desk, 'ins': json(ins)},
	        function(response){}
	    );
    });
    $(document).on('click', '.footer', function(){
	    window.location.replace('/customer-order?desk='+desk);
    });
    updater.poll();
});

function show_num(){
    var orders = myorder.orders;
    var left = myorder.left;
    var doing = myorder.doing;
    var done = myorder.done;
    var all = orders.concat(left, doing, done);
    $('.item').each(function(){
	    var did = $(this).attr('data-did');
	    var num = 0;
	    for(i in all) {
	        if(all[i].did == did) num += all[i].num;
	    }
	    $(this).find('.num').text(num);
    });
}
var updater = {
    interval: 800,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    var desk = $('.heading').attr('data-desk');
        console.log('polling', updater.cursor);
        updater.cursor += 1;
        updater.xhr = $.ajax({
            url: '/customer-update',
            type: 'POST',
            dataType: 'json',
            data: {'desk': desk, 'stamp': json(updater.stamp)},
            success: updater.onSuccess,
            error: updater.onError
        });

    },
    onSuccess: function(response){
        window.myorder = response.myorder;
        updater.stamp = myorder.stamp;
        show_num();
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
