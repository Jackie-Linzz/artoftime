$(document).ready(function(){
    window.myorder = {};
    window.delete = '';
    $('.prompt').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/cashier-home');
    });
    $(document).on('tap', '.input-button', function(){
	var desk = $('#input').val();
	desk = trim(desk);
	if(desk == '') return;
	$.postJSON(
	    '/cashier-work-desk',
	    {'desk': desk},
	    function(response){
		if(response.status != 'ok') return;
		window.myorder = response.myorder;
		show_content();
	    }
	);
    });
    $(document).on('tap', '.item .button', function(){
	var uid = $(this).parents('.item').data('uid');
	window.delete = uid;
	$('.prompt').show();
    });
    $(document).on('tap', '.ok-button', function(){
	var uid = window.delete;
	$.postJSON(
	    '/cashier-work-delete',
	    {'uid': uid},
	    function(response){
		if(response.status != 'ok') return;
		window.myorder = response.myorder;
		show_content();
	    }
	);
    });
    $(document).on('tap', '.cancel-button', function(){
	window.delete = '';
	$('.prompt').hide();
    });
    $(document).on('tap', '.footer', function(){
	var desk = trim($('#input').val());
	$.postJSON(
	    '/cashier-work-cash',
	    {'desk': desk},
	    function(response){
		if(response.status != 'ok') return;
	    }
	);
    });
});

function show_content() {
    
    var left = myorder.left;
    var doing = myorder.doing;
    var done = myorder.done;
    var cancel = myorder.cancel;

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
    
    $('.total').find('.price').text(total);
    $('.total').find('.num').text(num);
    $('.gdemand').val(myorder.gdemand);
}
