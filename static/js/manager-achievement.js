$(document).ready(function(){
    $('.cashier').hide();
    $('.cook').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/manager-home');
    });
    $(document).on('tap', '.button', function(){
	var from = $('#from').val();
	var to = $('#to').val();
	var fid = $('#fid').val();

	from = trim(from);
	to = trim(to);
	fid = trim(fid);

	if(from == '') return;
	if(to == '') return;
	if(fid == '') return;

	$.postJSON(
	    '/manager-achievement',
	    {'fid': fid, 'from': from, 'to': to},
	    function(response) {
		if(response.status != 'ok') return;
		var roles = response.roles;
		for(var i in roles) {
		    if(roles[i] == 'cashier') {
			$('.cashier').show();
			var p = $('.cashier tbody').empty();
			var cashier = response.cashier;
			console.log(cashier);
			var tr = $('<tr><td>'+cashier.failure+'</td><td>'+cashier.success+'</td></tr>');
			p.append(tr);
			
		    }
		    if(roles[i] == 'cook') {
			$('.cook').show();
			var p = $('.flow tbody').empty();
			var flow = response.flow;
			for(var k in flow) {
			    var one = flow[k];
			    var tr = $('<tr><td>'+one.name+'</td><td>'+one.number+'</td></tr>');
			    p.append(tr);
			}
			p = $('.fb tbody').empty();
			var fb = response.fb;
			for(var k in fb) {
			    var one = fb[k];
			    var tr = $('<tr><td>'+one.name+'</td><td>'+one.good+'</td><td>'+one.normal+'</td><td>'+one.bad+'</td><td>'+one.goodrate+'</td><td>'+one.badrate+'</td></tr>');
			    p.append(tr);
			}
		    }
		}
		
	    }
	);
    });
});
