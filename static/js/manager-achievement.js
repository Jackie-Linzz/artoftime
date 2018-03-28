$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }

    $('.result').hide();
    window.faculty = [];
    window.result = [];
    $.postJSON(
        '/manager-faculty-list',
        {},
        function(response) {
            window.faculty = [];
            for(var i in response.faculty) {
                var one = response.faculty[i];
                if(/cook/i.test(one.role)) window.faculty.push(one);
            }
            show_select();
        }
    );
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $('#fid').val('all');
    $(document).on('change', 'select', function(){
        var fid = $(this).val();
        $('#fid').val(fid);
    });
    $(document).on('change', '#trend', function(){
        console.log($(this).prop('checked'));
    });
    $(document).on('click', '.button', function(){
	    $('.result').hide();

	    var from = $('#from').val();
	    var to = $('#to').val();
	    var fid = $('#fid').val();
        var trend = $('#trend').prop('checked');

	    from = trim(from);
	    to = trim(to);
	    fid = trim(fid);

	    if(from == '') return;
	    if(to == '') return;
	    if(fid == '') return;

        if(fid == 'all' && trend == true) return;
        if(trend) {
            trend = 1;
        } else {
            trend = 0;
        }
	    $.postJSON(
	        '/manager-achievement',
	        {'fid': fid, 'from': from, 'to': to, 'trend': trend},
	        function(response) {
		        if(response.status != 'ok') return;
                window.result = response.result;
                show_result();
                $('.result').show();
	        }
	    );
    });
});

function show_select() {
    $('.append').remove();
    var p = $('select');
    for(var i in window.faculty) {
        one = window.faculty[i];
        var option = $('<option class="append" value="'+one.fid+'">'+one.fid+':'+one.name+'</option>');
        p.append(option);
    }
}
function show_result(){
    var p = $('.result').empty();
    for(var i in window.result){
        var table = window.result[i];
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
