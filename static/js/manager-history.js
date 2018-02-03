$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	var css = $('#css').attr('href');
	css = css.replace(/-mobile/g, '');
	$('#css').attr('href', css);
    }
    $('.tab').hide();
    $(document).on('tap', '.back', function(){
	window.location.replace('/manager-home');
    });
    $(document).on('tap', '.flow .op', function(){
	$('.tab').hide();
	$('.flow-content').show();
	$('.flow-content table').hide();
    });
    $(document).on('tap', '.fb .op', function(){
	$('.tab').hide();
	$('.fb-content').show();
	$('.fb-content table').hide();
    });
    $(document).on('tap', '.trend .op', function(){
	$('.tab').hide();
	$('.trend-content').show();
	$('.trend-content table').hide();
    });
    $(document).on('tap', '#flow-query', function(){
	$('.flow-content table').hide();
	
	var from = $('#flow-from').val();
	var to = $('#flow-to').val();

	from = trim(from);
	to = trim(to);

	if(from == '') return;
	if(to == '') return;

	$.postJSON(
	    '/manager-history-flow',
	    {'from': from, 'to': to},
	    function(response) {
		if(response.status != 'ok') return;
		$('.flow-content table').show();
		var flow = response.flow;
		//console.log(flow);
		var p = $('.flow-content tbody').empty();
		var all_flow = 0;
		var all_num = 0;
		for(var i in flow) {
		    var one = flow[i];
		    var tr = $('<tr>'+
			    '<td class="did"></td>'+
			    '<td class="name"></td>'+
			    '<td class="price"></td>'+
			    '<td class="num"></td>'+
			    '<td class="fl"></td>'+
			       '</tr>');
		    var fl = one.total;
		    all_flow += fl;
		    all_num += one.number;
		    tr.find('.did').text(one.did);
		    tr.find('.name').text(one.name);
		    tr.find('.price').text(one.price);
		    tr.find('.num').text(one.number);
		    tr.find('.fl').text(fl);
		    p.append(tr);
		}
		var last = $('<tr>'+
			     '<td class="did"></td>'+
			     '<td class="name"></td>'+
			     '<td class="price"></td>'+
			     '<td class="num"></td>'+
			     '<td class="fl"></td>'+
			     '</tr>');
		last.find('.did').text('');
		last.find('.name').text('全部');
		last.find('price').text('');
		last.find('.num').text(all_num);
		last.find('.fl').text(all_flow);
		p.append(last);
	    }
	);
    });
    $(document).on('tap', '#fb-query', function(){
	$('.fb-content table').hide();
	
	var from = $('#fb-from').val();
	var to = $('#fb-to').val();

	from = trim(from);
	to = trim(to);

	if(from == '') return;
	if(to == '') return;

	$.postJSON(
	    '/manager-history-fb',
	    {'from': from, 'to': to},
	    function(response) {
		if(response.status != 'ok') return;
		$('.fb-content table').show();
		var fb = response.fb;
		var p = $('.fb-content tbody').empty();
		var all_num = 0;
		var all_good = 0;
		var all_normal = 0;
		var all_bad = 0;
		for(var i in fb) {
		    var one = fb[i];
		    
		    var num = one.good+one.normal+one.bad;
		    var goodrate = 0;
		    var badrate = 0;
		    if(num == 0) {
			goodrate = 0;
			badrate = 0;
		    } else {
			goodrate = one.good*100/num;
			badrate = one.bad*100/num;
		    }
		    
		    all_num += num;
		    all_good += one.good;
		    all_normal += one.normal;
		    all_bad += one.bad;
		    
		    var tr = $('<tr>'+
			       '<td class="did">0001</td>'+
			       '<td class="name">coffee</td>'+
			       '<td class="num">100</td>'+
			       '<td class="good">1</td>'+
			       '<td class="normal">98</td>'+
			       '<td class="bad">1</td>'+
			       '<td class="goodrate">1%</td>'+
			       '<td class="badrate">1%</td>'+
			       '</tr>');
		    tr.find('.did').text(one.did);
		    tr.find('.name').text(one.name);
		    tr.find('.num').text(num);
		    tr.find('.good').text(one.good);
		    tr.find('.normal').text(one.normal);
		    tr.find('.bad').text(one.bad);
		    tr.find('.goodrate').text(goodrate+'%');
		    tr.find('.badrate').text(badrate+'%');
		    p.append(tr);
		}
		var last = $('<tr>'+
			     '<td class="did">0001</td>'+
			     '<td class="name">coffee</td>'+
			     '<td class="num">100</td>'+
			     '<td class="good">1</td>'+
			     '<td class="normal">98</td>'+
			     '<td class="bad">1</td>'+
			     '<td class="goodrate">1%</td>'+
			     '<td class="badrate">1%</td>'+
			     '</tr>');
		if(all_num == 0) {
		    goodrate = 0;
		    badrate = 0;
		} else {
		    goodrate = all_good*100/all_num;
		    badrate = all_bad*100/all_num;
		}
		
		last.find('.did').text('');
		last.find('.name').text('全部');
		last.find('.num').text(all_num);
		last.find('.good').text(all_good);
		last.find('.normal').text(all_normal);
		last.find('.bad').text(all_bad);
		last.find('.goodrate').text(goodrate+'%');
		last.find('.badrate').text(badrate+'%');
		p.append(last);
	    }
	);
    });
    $(document).on('tap', '#trend-query', function(){
	$('.trend-content table').hide();
	
	var from = $('#trend-from').val();
	var to = $('#trend-to').val();

	from = trim(from);
	to = trim(to);

	if(from == '') return;
	if(to == '') return;

	$.postJSON(
	    '/manager-history-trend',
	    {'from': from, 'to': to},
	    function(response) {
		if(response.status != 'ok') return;
		$('.trend-content table').show();

		var trend = response.trend;
		var p = $('.trend-content tbody').empty();

		for(var i in trend) {
		    var one = trend[i];
		    var tr = $('<tr>'+
			    '<td class="from">2017.1.1</td>'+
			    '<td class="to">2017.2.1</td>'+
			    '<td class="f">10000</td>'+
			       '</tr>');
		    tr.find('.from').text(one.from);
		    tr.find('.to').text(one.to);
		    tr.find('.f').text(one.flow);
		    p.append(tr);
		}
	    }
	);
    });
});
