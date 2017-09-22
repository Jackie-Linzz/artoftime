$(document).ready(function(){
    $('.tab').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/manager-home');
    });
    $(document).on('tap', '.group .add', function(){
	$('.tab').hide();
	$('.group-add').show();
    });
    $(document).on('tap', '.group .delete', function(){
	$('.tab').hide();
	$('.group-del').show();
    });
    $(document).on('tap', '.group .show', function(){
	$('.tab').hide();
	$('.group-show').show();
	$.postJSON(
	    '/manager-group-show',
	    {},
	    function(response) {
		if(response.status != 'ok') return;
		var category = response.category;
		var p = $('.group-show tbody').empty();
		for(var i in category) {
		    var tr = $('<tr>'+
			    '<td class="cid"></td>'+
			    '<td class="name"></td>'+
			    '<td class="order"></td>'+
			    '<td class="desp"></td>'+
			       '</tr>');
		    //console.log(category[i]);
		    tr.find('.cid').text(category[i].cid);
		    tr.find('.name').text(category[i].name);
		    tr.find('.order').text(category[i].ord);
		    tr.find('.desp').text(category[i].desp);
		    p.append(tr);
		}
	    }
	);
	
    });
    $(document).on('tap', '.diet .add', function(){
	$('.tab').hide();
	$('.diet-add').show();
    });
    $(document).on('tap', '.diet .delete', function(){
	$('.tab').hide();
	$('.diet-del').show();
    });
    $(document).on('tap', '.diet .show', function(){
	$('.tab').hide();
	$('.diet-show').show();
	$.postJSON(
	    '/manager-diet-show',
	    {},
	    function(response) {
		if(response.status != 'ok') return;
		var diet = response.diet;
		var p = $('.diet-show tbody').empty();
		for(var i in diet) {
		    var tr = $('<tr>'+
			    '<td class="did"></td>'+
			    '<td class="name"></td>'+
			    '<td class="order"></td>'+
			    '<td class="price"></td>'+
			    '<td class="cid"></td>'+
			    '<td class="detail">...</td>'+
			       '</tr>');
		    tr.data(diet[i]);
		    tr.find('.did').text(diet[i].did);
		    tr.find('.name').text(diet[i].name);
		    tr.find('.order').text(diet[i].ord);
		    tr.find('.price').text(diet[i].price);
		    tr.find('.cid').text(diet[i].cid);
		    p.append(tr);
		}
	    }
	);
    });
    $(document).on('tap', '#group-add-button', function(){
	var cid = $('#cid').val();
	var cname = $('#c-name').val();
	var corder = $('#c-order').val();
	var cdesp = $('#c-desp').val();
	cid = trim(cid);
	cname = trim(cname);
	corder = trim(corder);
	cdesp = trim(cdesp);
	$.postJSON(
	    '/manager-group-add',
	    {'cid': cid, 'cname': cname, 'corder': corder, 'cdesp': cdesp},
	    function(response){
		if(response.status == 'ok') {
		    $('#cid').val('');
		    $('#c-name').val('');
		    $('#c-order').val('');
		    $('#c-desp').val('');
		}
	    }
	);
    });
    $(document).on('tap', '#group-del-button', function(){
	var cid = $('#cid2').val();
	cid = trim(cid);
	$.postJSON(
	    '/manager-group-del',
	    {'cid': cid},
	    function(response){
		if(response.status == 'ok') {
		    $('#cid2').val('');
		}
	    }
	);
    });
    $(document).on('tap', '#diet-del-button', function(){
	var did = $('#did2').val();
	did = trim(did);
	$.postJSON(
	    '/manager-diet-del',
	    {'did': did},
	    function(response) {
		if(response.status == 'ok') {
		    $('#did2').val('');
		}
	    }
	);
    });
    $(document).on('tap', '.detail', function(){
	$('.diet-detail').show();
	var tr = $(this).parents('tr');
	$('.diet-detail .did').text(tr.data('did'));
	$('.diet-detail .name').text(tr.data('name'));
	$('.diet-detail img').attr('src', '/static/pictures/'+tr.data('pic'));
	$('.diet-detail .price').text(tr.data('price'));
	$('.diet-detail .price2').text(tr.data('price2'));
	$('.diet-detail .order').text(tr.data('ord'));
	$('.diet-detail .base').text(tr.data('base'));
	$('.diet-detail .cid').text(tr.data('cid'));
	$('.diet-detail .desp').text(tr.data('desp'));
    });
    $(document).on('tap', '.diet-detail .close', function(){
	$('.diet-detail').hide();
    });
});
