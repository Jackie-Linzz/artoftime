$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $('.tab').hide();
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '.group .add', function(){
	    $('.tab').hide();
	    $('.group-add').show();
    });
    $(document).on('click', '.group .delete', function(){
	    $('.tab').hide();
	    $('.group-del').show();
    });
    $(document).on('click', '.group .show', function(){
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
    $(document).on('click', '.diet .add', function(){
	    $('.tab').hide();
	    $('.diet-add').show();
    });
    $(document).on('click', '.diet .delete', function(){
	    $('.tab').hide();
	    $('.diet-del').show();
    });
    $(document).on('click', '.diet .show', function(){
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
    $(document).on('click', '#group-add-button', function(){
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
    $(document).on('click', '#group-del-button', function(){
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
    $(document).on('click', '#diet-add-button', function(){
	    var did = trim($('#did').val());
	    var name = trim($('#d-name').val());
	    var order = trim($('#d-order').val());
	    var price = trim($('#d-price').val());
	    var price2 = trim($('#d-price2').val());
	    var base = trim($('#d-base').val());
	    var cid = trim($('#d-cid').val());
        var who = trim($('#d-who').val());
	    var desp = trim($('#d-desp').val());
	    if(did == '' || name == '' || order == '' || price == '' || price2 == '' || base == '' || cid == '') return;
	    var formdata = new FormData($('#diet-add-form')[0]);
	    $.ajax({
	        url: '/manager-diet-add',
	        type: 'POST',
	        cache: false,
	        data: formdata,
	        dataType: 'json',
	        processData: false,
	        contentType: false,
	        success: function(response) {
		        if(response.status != 'ok') return;
		        $('#did').val('');
		        $('#d-name').val('');
		        $('#d-order').val('');
		        $('#d-price').val('');
		        $('#d-price2').val('');
		        $('#d-base').val('');
		        $('#d-cid').val('');
                $('#d-who').attr('checked', false);
		        $('#d-pic').val('');
		        $('#d-desp').val('');
	        },
	        error: function(response) {
		        console.log('ERROR:', response);
	        }
	    });
    });
    $(document).on('click', '#diet-del-button', function(){
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
    $(document).on('click', '.detail', function(){
	    $('.diet-detail').show();
	    var tr = $(this).parents('tr');
	    $('.diet-detail .did').text(tr.data('did'));
	    $('.diet-detail .name').text(tr.data('name'));
	    $('.diet-detail img').attr('src', '/pictures/'+tr.data('pic'));
	    $('.diet-detail .price').text(tr.data('price'));
	    $('.diet-detail .price2').text(tr.data('price2'));
	    $('.diet-detail .order').text(tr.data('ord'));
	    $('.diet-detail .base').text(tr.data('base'));
	    $('.diet-detail .cid').text(tr.data('cid'));
	    $('.diet-detail .desp').text(tr.data('desp'));
        if(tr.data('who') == 'cook') {
            $('.diet-detail .who').text('厨师');
        } else {
            $('.diet-detail .who').text('服务员');
        }
    });
    $(document).on('click', '.diet-detail .close', function(){
	    $('.diet-detail').hide();
    });
});
