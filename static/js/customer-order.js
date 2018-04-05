$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.myorder = {};
    var desk = $('.heading').attr('data-desk');
    $('.one').remove();
    $(document).on('click', '.left', function(){
	    window.location.replace('/customer-home?desk='+desk);
    });
    $(document).on('click', '.item .button', function(){
	    var uid = $(this).parents('.item').data('uid');
	    var ins = ['-', uid];
	    $.postJSON(
	        '/customer-ins',
	        {'desk': desk, 'ins': json(ins)},
	        function(){}
	    );
    });
    $(document).on('change', '.gdemand', function(){
	    //input propertychange
	    var gdemand = $('.gdemand').val();
	    gdemand = trim(gdemand);
	    var ins = ['g', gdemand];
	    $.postJSON(
	        '/customer-ins',
	        {'desk': desk, 'ins': json(ins)},
	        function(){}
	    );
    });
    $(document).on('click', '.footer', function(){
	    //$(this).addClass('animation');
	    var ins = ['submit'];
	    $.postJSON(
	        '/customer-ins',
	        {'desk': desk, 'ins': json(ins)},
	        function(){}
	    );
    });
    updater.poll();
});
function Item(data) {
    var item = $('<div class="item one">'+
		         '<div class="row">'+
                 '<div class="name">名字</div><!--'+
		         '--><div class="price">18.0</div><!--'+
		         '--><div class="num">0</div>'+
		         '</div>'+
		         '<div class="row">'+
                 '<div class="demand">这是特殊要求</div>'+
		         '</div>'+
		         '<div class="row">'+
                 ' <div class="button">x</div>'+
		         '</div>'+
		         '</div>');
    item.data(data);
    item.find('.name').text(data.name);
    item.find('.price').text(data.price);
    item.find('.num').text(data.num);
    item.find('.demand').text(data.demand);
    if(data.demand == '') item.find('.demand').remove();
    return item;
}

function show_order(){
    var orders = myorder.orders;
    var left = myorder.left;
    var doing = myorder.doing;
    var done = myorder.done;


    $('.one').remove();
    var num = 0;
    var total = 0;
    for(i in done) {
	    var one = done[i]
	    num += one.num;
	    total += one.price * one.num;
	    var item = Item(one);
	    item.find('.name').text(one.name+'(已做)');
	    item.find('.button').remove();
	    $('.total').before(item);
    }
    for(i in doing) {
	    var one = doing[i]
	    num += one.num;
	    total += one.price * one.num;
	    var item = Item(one);
	    item.find('.name').text(one.name+'(在做)');
	    item.find('.button').remove();
	    $('.total').before(item);
    }
    for(i in left) {
	    var one = left[i]
	    num += one.num;
	    total += one.price * one.num;
	    var item = Item(one);
	    item.find('.name').text(one.name+'(待做)');
	    item.find('.button').remove();
	    $('.total').before(item);
    }
    for(i in orders) {
	    var one = orders[i]
	    num += one.num;
	    total += one.price * one.num;
	    var item = Item(one);
	    item.find('.name').text(one.name);
	    $('.total').before(item);
    }
    $('.total').find('.price').text(total.toFixed(2));
    $('.total').find('.num').text(num);
    $('.gdemand').val(myorder.gdemand);

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
