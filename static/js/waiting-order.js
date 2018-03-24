$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.myorder = {};
    $(document).on('tap', '.left', function(e){
	    window.location.replace('/waiting-category');
    });
    $(document).on('input propertychange', '.gdemand', function(){
	    var gdemand = $('.gdemand').val();
	    gdemand = trim(gdemand);
	    var ins = ['g', gdemand];
	    $.postJSON(
	        '/waiting-ins',
	        {'ins': json(ins)},
	        function(){}
	    );
    });
    updater.poll();
});
function Item(data) {
    var item$ = $('<div class="item one">'+
                  '<div class="row">'+
                  '<div class="name"></div><!--'+
                  '--><div class="price"></div><!--'+
                  '--><div class="num"></div>'+
                  '</div>'+
                  '<div class="row">'+
                  '<div class="demand"></div>'+
                  '</div>'+
                  '<div class="row">'+
                  '<div class="button">-</div>'+
                  '</div>'+
		          '</div>');
    item$.data(data);
    item$.find('.name').text(data.name);
    item$.find('.price').text(data.price);
    item$.find('.num').text(data.num);
    item$.find('.demand').val(data.demand);
    return item$;
}

function show_order() {

    $('.one').remove();
    var last = $('.total');
    var num = 0;
    var total = 0;
    for(i in window.myorder.orders) {
	    var one = myorder.orders[i];
	    num += one.num;
	    total += one.price * one.num;
	    var item$ = Item(one);
	    last.before(item$);
    }
    last.find('.price').text(total);
    last.find('.num').text(num);
    $('.gdemand').val(myorder.gdemand);
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
        updater.stamp = response.stamp;
        show_order();
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
