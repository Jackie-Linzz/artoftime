$(document).ready(function(){
    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.flow = [];
    window.frequency = [];
    window.cooks = [];
    $(document).on('click', '.back', function(){
        window.location.replace('/manager-home');
    });
    $('.content').empty();
    $.postJSON(
        '/manager-today',
        {},
        function(response){
            window.flow = response.flow;
            window.frequency = response.frequency;
            window.cooks = response.cooks;
            show_content();
        }
    );
});
function show_content() {
    $('.content').empty();
    show_flow();
    show_frequency();
    show_cooks();
}
function show_flow(){
    var p = $('.content');
    for(var i in window.flow){
        var table = window.flow[i];
        var table$ = $('<table border="1" cellspacing="0">'+
		               '<caption>今日流水</caption>'+
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
            all_fb_num = row['fb-num'];
            all_good = row['good-num'];
            all_bad = row['bad-num'];
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
function show_frequency(){
    var p = $('.content');
    for(var i in window.frequency) {
        var table = window.frequency[i];
        /* console.log(table);*/
        var table$ = $('<table border="1" cellspacing="0">'+
		               '<caption></caption>'+
		               '<thead>'+
			           '<tr>'+
			           '<th>从</th>'+
			           '<th>到</th>'+
			           '<th>数量</th>'+
			           '</tr>'+
		               '</thead>'+
		               '<tbody>'+
		               '</tbody>'+
		               '</table>');
        if(table.type == 'request') {
            table$.find('caption').text('顾客请求');
        } else if (table.type == 'kitchen') {
            table$.find('caption').text('厨房');
        } else if (table.type == 'cash') {
            table$.find('caption').text('收银');
        }
        var tbody = table$.find('tbody');
        for(var j in table.rows) {
            var row = table.rows[j];
            var tr = $('<tr>'+
			           '<td class="from">time</td>'+
			           '<td class="to">time</td>'+
			           '<td class="num">num</td>'+
			           '</tr>');
            tr.find('.from').text(row.from);
            tr.find('.to').text(row.to);
            tr.find('.num').text(row.num);
            tbody.append(tr);
        }
        p.append(table$);
    }
}
function show_cooks(){
    var p = $('.content');
    for(var i in window.cooks){
        var table = window.cooks[i];
        //console.log(table);
        var table$ = $('<table border="1" cellspacing="0" class="fb">'+
		               '<caption>统计</caption>'+
		               '<thead>'+
			           '<tr>'+
			           '<th>名字</th>'+
                       '<th>数量</th>'+
                       '<th>反馈数量</th>'+
			           '<th>好吃</th>'+
			           '<th>一般</th>'+
			           '<th>难吃</th>'+
			           '<th>好评率</th>'+
			           '<th>差评率</th>'+
			           '</tr>'+
		               '</thead>'+
		               '<tbody>'+
			           '<tr>'+
			           '<td>coffee</td>'+
                       '<td>100</td>'+
                       '<td>100</td>'+
			           '<td>1</td>'+
			           '<td>98</td>'+
			           '<td>1</td>'+
			           '<td>1%</td>'+
			           '<td>1%</td>'+
			           '</tr>'+
		               '</tbody>'+
		               '</table>');
        if(table.type == 'all') {
            table$.find('caption').text('统计所有');
        } else if(table.type == 'all-time'){
            table$.find('caption').text(table.from+':'+table.to+':统计所有');
        } else if(table.type == 'cook'){
            table$.find('caption').text(table.fid+':'+table.name);
        } else if(table.type == 'cook-time') {
            table$.find('caption').text(table.from+':'+table.to+':'+table.name);
        }
        var tbody$ = table$.find('tbody').empty();
        var all_num = 0;
        var all_fb_num = 0;
        var all_good_num = 0;
        var all_normal_num = 0;
        var all_bad_num = 0;
        for(var j in table.rows){
            var row = table.rows[j];
            all_num += row.num;
            all_fb_num += row['fb-num'];
            all_good_num += row['good-num'];
            all_normal_num += row['normal-num'];
            all_bad_num += row['bad-num'];
            var tr$ = $('<tr>'+
			            '<td class="name">coffee</td>'+
                        '<td class="num">100</td>'+
                        '<td class="fb-num">100</td>'+
			            '<td class="good-num">1</td>'+
			            '<td class="normal-num">98</td>'+
			            '<td class="bad-num">1</td>'+
			            '<td class="good-rate">1%</td>'+
			            '<td class="bad-rate">1%</td>'+
			            '</tr>');
            tr$.find('.name').text(row.name);
            tr$.find('.num').text(row.num);
            tr$.find('.fb-num').text(row['fb-num']);
            tr$.find('.good-num').text(row['good-num']);
            tr$.find('.normal-num').text(row['normal-num']);
            tr$.find('.bad-num').text(row['bad-num']);
            tr$.find('.good-rate').text(row['good-rate'].toFixed(2)+'%');
            tr$.find('.bad-rate').text(row['bad-rate'].toFixed(2)+'%');
            tbody$.append(tr$);
        }
        var all_good_rate = 0;
        var all_bad_rate = 0;
        if(all_fb_num != 0){
            all_good_rate = all_good_num*100/all_fb_num;
            all_bad_rate = all_bad_num*100/all_fb_num;
        }
        
        var tr$ = $('<tr>'+
			        '<td class="name">coffee</td>'+
                    '<td class="num">100</td>'+
                    '<td class="fb-num">100</td>'+
			        '<td class="good-num">1</td>'+
			        '<td class="normal-num">98</td>'+
			        '<td class="bad-num">1</td>'+
			        '<td class="good-rate">1%</td>'+
			        '<td class="bad-rate">1%</td>'+
			        '</tr>');
        tr$.find('.name').text('共');
        tr$.find('.num').text(all_num);
        tr$.find('.fb-num').text(all_fb_num);
        tr$.find('.good-num').text(all_good_num);
        tr$.find('.normal-num').text(all_normal_num);
        tr$.find('.bad-num').text(all_bad_num);
        tr$.find('.good-rate').text(all_good_rate.toFixed(2)+'%');
        tr$.find('.bad-rate').text(all_bad_rate.toFixed(2)+'%');
        tbody$.append(tr$);
        p.append(table$);
    }
}
