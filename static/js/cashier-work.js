$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.myorder = {};
    window.delete = '';
    $('.prompt').hide();
    $('.message').hide();

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
	    $('.prompt').hide();
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
		        if(response.status == 'success') {
		            $('.message').show();
		            $('.message .msg').text('成功');
		            window.myorder = response.myorder;
		            show_content();
		        }
		        if(response.status == 'failure') {
		            $('.message').show();
		            $('.message .msg').text('失败，请等待所有订单完成！');
		            window.myorder = response.myorder;
		            show_content();
		        }
	        }
	    );
    });
    $(document).on('tap', '.message .button', function(){
	    $('.message').hide();
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

function show_content() {

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
	    item.find('.button').remove();
	    $('.total').before(item);
    }
    for(i in doing) {
	    var one = doing[i]
	    num += one.num;
	    total += one.price * one.num;
	    var item = Item(one);
	    item.find('.name').text(one.name+'(doing)');
	    item.find('.button').remove();
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

    $('.total').find('.price').text(total.toFixed(2));
    $('.total').find('.num').text(num);
    $('.gdemand').val(myorder.gdemand);
}
