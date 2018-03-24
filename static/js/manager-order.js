$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    }
    else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $('.order-show').hide();
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '.menu .query', function(){
	    $('.order-show').hide();
	    $('.query-order').show();
    });

    $(document).on('click', '#query-button', function(){
	    var order = $('#input-order').val();
	    order = trim(order);
	    if(order == '') return;
	    $.postJSON(
	        '/manager-order',
	        {'order': order},
	        function(response) {
		        if(response.status == 'ok') {
		            $('#input-order').val('');
                    $('.order-show').show();
                    var items = response.items;
                    var pid = response.pid;
                    $('caption').text(pid);
                    var p = $('table tbody').empty();
                    for(var i in items){
                        var one = items[i];
                        var tr = $('<tr>'+
			                       '<td class="name">0001</td>'+
			                       '<td class="num">0002</td>'+
			                       '<td class="price">0003</td>'+
			                       '<td class="cook">0004</td>'+
                                   '<td class="cashier">0004</td>'+
                                   '<td class="status">0004</td>'+
			                       '</tr>');
                        tr.find('.name').text(one.name);
                        tr.find('.num').text(one.num);
                        tr.find('.price').text(one.price);
                        tr.find('.cook').text(one.cook);
                        tr.find('.cashier').text(one.cashier);
                        tr.find('.status').text(one.status);
                        p.append(tr);

                    }
		        }
	        }
	    );
    });

});
