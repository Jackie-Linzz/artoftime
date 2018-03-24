$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.mask = [];

    $(document).on('click', '.back', function(){
	    window.location.replace('/waiter-home');
    });
    updater.poll();
});

function show_mask() {
    var p = $('.content').empty();
    for(var i in window.mask) {
	    var one = window.mask[i];
	    var item = $('<div class="item">did:name</div>');
	    item.data(one);//one is dict
	    item.text(one.did+':'+one.name+':'+one.cid);
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
            url: '/manager-mask-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(updater.stamp)},
            success: updater.onSuccess,
            error: updater.onError
        });

    },
    onSuccess: function(response){
        window.mask = response.mask;
        updater.stamp = response.stamp;
        show_mask();
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
