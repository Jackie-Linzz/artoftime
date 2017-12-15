$(document).ready(function(){
    window.myorder = {};
    window.desk = '';
    window.show = 1;
    $('.back').on('tap', function(){
	window.location.replace('/waiter-home');
    });
    $('#desk').on('focusout', function(){
	var desk = $(this).val().toUpperCase();
	
	window.desk = trim(desk);
	$(this).val(window.desk);
	if(updater.xhr) updater.reset();
	updater.poll();
    });
    $('#submit').on('tap', function(){
	var did = trim($('#did').val());
	var demand = trim($('#demand').val());
	if(window.desk == '') return;
	if(did == '') return;
	var ins = ['+', did, demand];
	$.postJSON(
	    '/waiter-ins',
	    {'desk': window.desk, 'ins': json(ins)},
	    function(response){
		if(response.status != 'ok') return;
		$('#did').val('');
		$('#demand').val('');
	    }
	);
    });
    $('.bar').on('tap', function(){
	if(window.show) {
	    $('.orders').hide();
	    window.show = 0;
	} else {
	    $('.orders').show();
	    window.show = 1;
	}
    });
    $(document).on('tap', '.item .button', function(){
	var uid = $(this).parents('.item').data('uid');
	var ins = ['-', uid];
	$.postJSON(
	    '/waiter-ins',
	    {'desk': window.desk, 'ins': json(ins)},
	    function(){}
	);
    });
    $(document).on('focusout', '.gdemand', function(){
	var gdemand = $(this).val();
	gdemand = trim(gdemand);
	var ins = ['g', gdemand];
	$.postJSON(
	    '/waiter-ins',
	    {'desk': window.desk, 'ins': json(ins)},
	    function(){}
	);
    });
    $(document).on('tap', '.submit', function(){
	var ins = ['submit'];
	$.postJSON(
	    '/waiter-ins',
	    {'desk': window.desk, 'ins': json(ins)},
	    function(){}
	);
    });
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
                 ' <div class="button">-</div>'+
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
	item.find('.name').text(one.name+'(done)');
	$('.total').before(item);
    }
    for(i in doing) {
	var one = doing[i]
	num += one.num;
	total += one.price * one.num;
	var item = Item(one);
	item.find('.name').text(one.name+'(doing)');
	$('.total').before(item);
    }
    for(i in left) {
	var one = left[i]
	num += one.num;
	total += one.price * one.num;
	var item = Item(one);
	item.find('.name').text(one.name+'(left)');
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
    $('.total').find('.price').text(total);
    $('.total').find('.num').text(num);
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
            url: '/waiter-order-update',
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
