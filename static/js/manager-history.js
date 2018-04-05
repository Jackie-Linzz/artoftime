$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.tables = [];
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });

    $('.flow-content').empty();
    $(document).on('click', '#flow-query', function(){
	    $('.flow-content').hide();

	    var from = $('#flow-from').val();
	    var to = $('#flow-to').val();
        var trend = $('#trend').prop('checked');

	    from = trim(from);
	    to = trim(to);

	    if(from == '') return;
	    if(to == '') return;

        if(trend){
            trend = 1;
        } else {
            trend = 0;
        }

	    $.postJSON(
	        '/manager-history-flow',
	        {'from': from, 'to': to, 'trend': trend},
	        function(response) {
		        if(response.status != 'ok') return;
		        $('.flow-content').show();
		        window.tables = response.result;
		        //console.log(flow);
		        show_tables();
	        }
	    );
    });


});

function show_tables(){
    var p = $('.flow-content').empty();
    for(var i in window.tables){
        var table = window.tables[i];
        var table$ = $('<table border="1" cellspacing="0">'+
		               '<caption>流水</caption>'+
		               '<thead>'+
			           '<tr>'+
			           '<th>编号</th>'+
			           '<th>名字</th>'+
			           '<th>价格</th>'+
			           '<th>数量</th>'+
                       '<th>数量百分比</th>'+
			           '<th>销售额</th>'+
                       '<th>销售额百分比</th>'+
                       '<th>反馈数量</th>'+
                       '<th>好评率</th>'+
                       '<th>中评率</th>'+
                       '<th>差评率</th>'+
			           '</tr>'+
		               '</thead>'+
		               '<tbody>'+			           
		               '</tbody>'+
		               '</table>');
        if(table.type = 'trend') {
            table$.find('caption').text(table.from+':'+table.to+':流水');
        }
        var tbody$ = table$.find('tbody').empty();
        var all_num = 0;
        var all_sales = 0;
        var all_fb_num = 0;
        var all_good = 0;
        var all_normal = 0;
        var all_bad = 0;
        for(var j in table.rows) {
            var row = table.rows[j];
            all_num += row.num;
            all_sales += row.sales;
            all_fb_num += row['fb-num'];
            all_good += row['good-num'];
            all_normal += row['normal-num'];
            all_bad += row['bad-num'];
            var tr = $('<tr>'+
			           '<td class="did">did</td>'+
			           '<td class="name">name</td>'+
			           '<td class="price">price</td>'+
			           '<td class="num">num</td>'+
			           '<td class="num-rate">rate</td>'+
                       '<td class="sales">sales</td>'+
                       '<td class="sales-rate">rate</td>'+
                       '<td class="fb-num">fb-num</td>'+
                       '<td class="good-rate">rate</td>'+
                       '<td class="normal-rate">rate</td>'+
                       '<td class="bad-rate">rate</td>'+
			           '</tr>');
            tr.find('.did').text(row.did);
            tr.find('.name').text(row.name);
            tr.find('.price').text(row.price);
            tr.find('.num').text(row.num);
            tr.find('.num-rate').text(row['num-rate'].toFixed(2)+'%');
            tr.find('.sales').text(row['sales']);
            tr.find('.sales-rate').text(row['sales-rate'].toFixed(2)+'%');
            tr.find('.fb-num').text(row['fb-num']);
            tr.find('.good-rate').text(row['good-rate'].toFixed(2)+'%');
            tr.find('.normal-rate').text(row['normal-rate'].toFixed(2)+'%');
            tr.find('.bad-rate').text(row['bad-rate'].toFixed(2)+'%');
            tbody$.append(tr);
        }
        
        var good_rate = all_good*100/all_fb_num;
        var normal_rate = all_normal*100/all_fb_num;
        var bad_rate = all_bad*100/all_fb_num;
        if(all_fb_num == 0) {
            good_rate = 0;
            normal_rate = 0;
            bad_rate = 0;
        }
        var tr = $('<tr>'+
			       '<td class="did">did</td>'+
			       '<td class="name">name</td>'+
			       '<td class="price">price</td>'+
			       '<td class="num">num</td>'+
			       '<td class="num-rate">rate</td>'+
                   '<td class="sales">sales</td>'+
                   '<td class="sales-rate">rate</td>'+
                   '<td class="fb-num">fb-num</td>'+
                   '<td class="good-rate">rate</td>'+
                   '<td class="normal-rate">rate</td>'+
                   '<td class="bad-rate">rate</td>'+
			       '</tr>');
        tr.find('.did').text('');
        tr.find('.name').text('共');
        tr.find('.price').text('');
        tr.find('.num').text(all_num);
        tr.find('.num-rate').text('100%');
        tr.find('.sales').text(all_sales);
        tr.find('.sales-rate').text('100%');
        tr.find('.fb-num').text(all_fb_num);
        tr.find('.good-rate').text(good_rate.toFixed(2)+'%');
        tr.find('.normal-rate').text(normal_rate.toFixed(2)+'%');
        tr.find('.bad-rate').text(bad_rate.toFixed(2)+'%');
        tbody$.append(tr);
        p.append(table$);
    }
}
