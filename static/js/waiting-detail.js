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
	    var cid = $(this).attr('data-cid');
	    window.location.replace('/waiting-diet?cid='+cid);
    });
    $(document).on('click', '.footer', function(e){
	    var did = $('.left').attr('data-did');
	    var demand = $('.demand').val();
	    demand = trim(demand);
	    var ins = ['+', did, demand];
	    $.postJSON(
	        '/waiting-ins',
	        {'ins': json(ins)},
	        function(response){}
	    );
    });
    updater.poll();
});
function show_num(){
    var did = $('.left').attr('data-did');
    var num = 0;
    var demand = '';
    for(i in window.myorder.orders){
	    var one = myorder.orders[i];
	    num += one.num;
	    demand = one.demand;
    }
    $('.num').text(num);
    $('.demand').val(demand);
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
