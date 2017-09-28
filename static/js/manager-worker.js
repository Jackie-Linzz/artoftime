$(document).ready(function(){
    $('.tab').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/manager-home');
    });
    $(document).on('tap', '.menu .add', function(){
	$('.tab').hide();
	$('.worker-add').show();
    });
    $(document).on('tap', '.menu .del', function(){
	$('.tab').hide();
	$('.worker-del').show();
    });
    $(document).on('tap', '.menu .show', function(){
	$('.tab').hide();
	$('.worker-show').show();
	$.postJSON(
	    '/manager-worker-show',
	    {},
	    function(response) {
		if(response.status != 'ok') return;
		var workers = response.workers;
		var p = $('.worker-show tbody').empty();
		for(var i in workers) {
		    var tr = $('<tr>'+
			    '<td class="fid">00001</td>'+
			    '<td class="name">jack</td>'+
			    '<td class="role">waiter</td>'+
			    '<td class="passwd">123456</td>'+
			       '</tr>');
		    tr.find('.fid').text(workers[i].fid);
		    tr.find('.name').text(workers[i].name);
		    tr.find('.role').text(workers[i].role);
		    tr.find('.passwd').text(workers[i].passwd);
		    p.append(tr);
		}
	    }
	);
    });
    $(document).on('tap', '#worker-add-button', function(){
	var fid = $('#fid').val();
	var name = $('#name').val();
	var passwd = $('#password').val();
	var box = [];
	$('input:checkbox:checked').each(function(){
	    box.push($(this).val());
	});
	//console.log(box);
	fid = trim(fid);
	name = trim(name);
	passwd = trim(passwd);

	if(fid == '') return;
	if(name == '') return;
	if(passwd == '') return;
	if(box == []) return;

	$.postJSON(
	    '/manager-worker-add',
	    {'fid': fid, 'name': name, 'passwd': passwd, 'role': json(box)},
	    function(response){
		if(response.status == 'ok') {
		    $('#fid').val('');
		    $('#name').val('');
		    $('#password').val('');
		    $('input:checkbox').attr('checked', false);
		    
		}
	    }
	);
	
    });
    $(document).on('tap', '#worker-del-button', function(){
	var fid = $('#fid2').val();
	fid = trim(fid);

	if(fid == '') return;

	$.postJSON(
	    '/manager-worker-del',
	    {'fid': fid},
	    function(response) {
		if(response.status == 'ok') {
		    $('#fid2').val('');
		}
	    }
	);
    });
});
