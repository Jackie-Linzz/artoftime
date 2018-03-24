$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.myorder = {};
    $(document).on('click', '.left', function(e){
	    window.location.replace('/waiting-category');
    });
    $('.item').on('click', '.detail', function(e){
	    var cid = $('.left').attr('data-cid');
	    var did = $(this).parents('.item').attr('data-did');
	    window.location.replace('/waiting-detail?cid='+cid+'&did='+did);
    });
    $('.item').on('click', '.button', function(e){
	    var did = $(this).parents('.item').attr('data-did');
	    var ins = ['+', did, ''];
	    $.postJSON(
	        '/waiting-ins',
	        {'ins': json(ins)},
	        function(){}
	    );
    });
    $(document).on('click', '.footer', function(e){
	    window.location.replace('/waiting-order');
    });
    updater.poll();
});
function show_num(){

    console.log('myorder: ', window.myorder);
    $('.item').each(function(index, element){
	    var num = 0;
	    var did = $(element).attr('data-did');
	    console.log('data-did: ', did, typeof(did));
	    for(i in window.myorder.orders){
	        var one = myorder.orders[i];
	        if(one.did == did) {
		        num += one.num;
		        console.log('equal');
	        }
	    }
	    $(element).find('.num').text(num);
    });
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
            url: '/waiting-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(updater.stamp)},
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
