$(document).ready(function(){
    $('.result1').hide();
    $('.result2').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/manager-home');
    });
    $(document).on('tap', '#cookdo-button', function(){
	var fid = $('#fid').val();
	fid = trim(fid);
	if(fid == '') return;
	$.postJSON(
	    '/manager-cookdo',
	    {'fid': fid},
	    function(response) {
		if(response.status == 'ok') {
		    if(response.result == 'all') {
			$('.result1').show();
			$('.result2').hide();
		    }
		    if(response.result == 'some') {
			$('.result1').hide();
			$('.result2').show();
			var cookdo = response.cookdo;
			var p = $('.result2 tbody').empty();
			for(var i in cookdo) {
			    var one = cookdo[i];
			    var tr = $('<tr><td class="did"></td><td class="name"></td><td class="cid"></td></tr>');
			    tr.find('.did').text(one.did);
			    tr.find('.name').text(one.name);
			    tr.find('.cid').text(one.cid);
			    p.append(tr);
			}
		    }
		}
	    }
	);
    });
});
