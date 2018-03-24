$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.diet = [];
    window.mask = [];
    $('.tab').hide();
    $.postJSON(
	    '/manager-mask-diet',
	    {},
	    function(response) {
	        if(response.status != 'ok') return;
	        diet = response.diet;
	        var p = $('.mask tbody').empty();
	        for(var i in diet) {
		        var one = diet[i];
		        var tr = $('<tr>'+
			               '<td class="did">0001</td>'+
			               '<td class="name">coffee</td>'+
			               '<td class="cid">group1</td>'+
			               '<td><input type="checkbox" class="did-mask"></td>'+
			               '</tr>');
		        tr.data(one);
		        tr.find('.did').text(one.did);
		        tr.find('.name').text(one.name);
		        tr.find('.cid').text(one.cid);
		        p.append(tr);
	        }
	    }
    );
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '.op1', function(){
	    $('.tab').hide();
	    $('.mask').show();
    });
    $(document).on('click', '.op2', function(){
	    $('.tab').hide();
	    $('.show').show();
    });
    $(document).on('click', '.did-mask', function(){
	    var flag = $(this).prop('checked');
	    var did = $(this).parents('tr').data('did');
	    //console.log('flag:', flag);
	    //console.log('did:', did);
	    var ins = [];
	    if(flag == true) {
	        ins = ['+', did];
	    } else {
	        ins = ['-', did];
	    }
	    console.log(ins);
	    $.postJSON(
	        '/manager-mask-ins',
	        {'ins': json(ins)},
	        function(response){}
	    );
    });
    updater.poll();
});
function show_mask() {
    while(window.diet == []) {}
    //$('.mask tbody tr .did-mask').attr('checked', false);
    $('.mask tbody tr').each(function(index, element){
	    //$(element).find('.did-mask').attr('checked', false);
	    var did = $(this).data('did');
	    //console.log('did:', did);
	    var flag = false;
	    for(var i in mask) {
	        if(mask[i].did == did) {
		        console.log('equal');
		        flag = true;

		        break;
	        }
	    }
	    $(element).find('.did-mask').attr('checked', flag);
    });
    //show part

    var p = $('.show tbody').empty();
    for(var i in window.mask) {
	    var one = window.mask[i];
	    var tr = $('<tr>'+
			       '<td class="did"></td>'+
			       '<td class="name"></td>'+
			       '<td class="cid"></td>'+
		           '</tr>');
	    tr.find('.did').text(one.did);
	    tr.find('.name').text(one.name);
	    tr.find('.cid').text(one.cid);
	    p.append(tr);
    }
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
            url: '/manager-mask-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(updater.stamp)},
            success: updater.onSuccess,
            error: updater.onError
        });

    },
    onSuccess: function(response){
        window.mask = response.mask;
        updater.stamp = response.stamp;
        show_mask();
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
