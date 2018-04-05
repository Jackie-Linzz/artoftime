$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }

    $('.result').hide();
    window.diet = [];
    window.result = [];
    $.postJSON(
        '/manager-diet-show',
        {},
        function(response) {
            window.diet = response.diet;
            show_select();
        }
    );
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });

    $(document).on('change', 'select', function(){
        var did = $(this).val();
        $('#did').val(did);
    });
    $(document).on('change', '#trend', function(){
        console.log($(this).prop('checked'));
    });
    $(document).on('click', '.button', function(){
	    $('.result').hide();

	    var from = $('#from').val();
	    var to = $('#to').val();
	    var did = $('#did').val();
        var trend = $('#trend').prop('checked');

	    from = trim(from);
	    to = trim(to);
	    did = trim(did);

	    if(from == '') return;
	    if(to == '') return;
	    if(did == '') return;


        if(trend) {
            trend = 1;
        } else {
            trend = 0;
        }
	    $.postJSON(
	        '/manager-onediet',
	        {'did': did, 'from': from, 'to': to, 'trend': trend},
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
    $('option').remove();
    if(window.diet.length == 0) return;
    $('#did').val(window.diet[0].did);
    var p = $('select');
    for(var i in window.diet) {
        one = window.diet[i];
        var option = $('<option  value="'+one.did+'">'+one.did+':'+one.name+'</option>');
        p.append(option);
    }
}
function show_result(){
    var p = $('.result').empty();
    for(var i in window.result){
        var data = window.result[i];
        var table = $('<table border="1" cellspacing="0">'+
		              '<caption>销售</caption>'+
		              '<thead>'+
			          '<tr>'+
			          '<th>名字</th>'+
                      '<th>价格</th>'+
                      '<th>数量</th>'+
                      '<th>总量</th>'+
			          '<th>数量百分比</th>'+
			          '<th>销售额</th>'+
			          '<th>总销售额</th>'+
			          '<th>销售额百分比</th>'+
			          '</tr>'+
		              '</thead>'+
		              '<tbody>'+
			          '<tr>'+
			          '<td class="name"></td>'+
                      '<td class="price"></td>'+
                      '<td class="num">100</td>'+
                      '<td class="all-num">100</td>'+
			          '<td class="num-rate">1</td>'+
			          '<td class="sales">98</td>'+
			          '<td class="all-sales">1</td>'+
			          '<td class="sales-rate">1%</td>'+
			          '</tr>'+
		              '</tbody>'+
		              '</table>');
        table.find('caption').text(data.from+":"+data.to+':销售');
        table.find('.name').text(data.name);
        table.find('.price').text(data.price);
        table.find('.num').text(data.num);
        table.find('.all-num').text(data['all-num']);
        table.find('.num-rate').text(data['num-rate'].toFixed(2)+'%');
        table.find('.sales').text(data.sales);
        table.find('.all-sales').text(data['all-sales']);
        table.find('.sales-rate').text(data['sales-rate'].toFixed(2)+'%');
        p.append(table);
        table = $('<table border="1" cellspacing="0">'+
		          '<caption>反馈</caption>'+
		          '<thead>'+
			      '<tr>'+
			      '<th>名字</th>'+
                  '<th>反馈数量</th>'+
                  '<th>好评</th>'+
			      '<th>中评</th>'+
			      '<th>差评</th>'+
			      '<th>好评率</th>'+
                  '<th>中评率</th>'+
			      '<th>差评率</th>'+
			      '</tr>'+
		          '</thead>'+
		          '<tbody>'+
			      '<tr>'+
			      '<td class="name"></td>'+
                  '<td class="fb-num">100</td>'+
                  '<td class="good-num">100</td>'+
			      '<td class="normal-num">1</td>'+
			      '<td class="bad-num">98</td>'+
			      '<td class="good-rate">1</td>'+
                  '<td class="normal-rate"></td>'+
			      '<td class="bad-rate">1%</td>'+
			      '</tr>'+
		          '</tbody>'+
		          '</table>');
        table.find('caption').text(data.from+":"+data.to+':反馈');
        table.find('.name').text(data.name);
        table.find('.fb-num').text(data['fb-num']);
        table.find('.good-num').text(data['good-num']);
        table.find('.normal-num').text(data['normal-num']);
        table.find('.bad-num').text(data['bad-num']);
        table.find('.good-rate').text(data['good-rate'].toFixed(2)+'%');
        table.find('.normal-rate').text(data['normal-rate'].toFixed(2)+'%');
        table.find('.bad-rate').text(data['bad-rate'].toFixed(2)+'%');
        var tr = $('<tr>'+
			       '<td class="name"></td>'+
                   '<td class="fb-num">100</td>'+
                   '<td class="good-num">100</td>'+
			       '<td class="normal-num">1</td>'+
			       '<td class="bad-num">98</td>'+
			       '<td class="good-rate">1</td>'+
                   '<td class="normal-rate"></td>'+
			       '<td class="bad-rate">1%</td>'+
			       '</tr>');
        tr.find('.name').text('所有');
        tr.find('.fb-num').text(data['all-fb-num']);
        tr.find('.good-num').text(data['all-good-num']);
        tr.find('.normal-num').text(data['all-normal-num']);
        tr.find('.bad-num').text(data['all-bad-num']);
        tr.find('.good-rate').text(data['all-good-rate'].toFixed(2)+'%');
        tr.find('.normal-rate').text(data['all-normal-rate'].toFixed(2)+'%');
        tr.find('.bad-rate').text(data['all-bad-rate'].toFixed(2)+'%');
        table.find('tbody').append(tr);
        p.append(table);
        table = $('<table border="1" cellspacing="0">'+
		          '<caption>厨师关系</caption>'+
		          '<thead>'+
			      '<tr>'+
			      '<th>厨师编号</th>'+
                  '<th>名字</th>'+
                  '<th>数量</th>'+
			      '<th>反馈数量</th>'+
			      '<th>好评</th>'+
			      '<th>中评</th>'+
			      '<th>差评</th>'+
                  '<th>好评率</th>'+
                  '<th>中评率</th>'+
                  '<th>差评率</th>'+
			      '</tr>'+
		          '</thead>'+
		          '<tbody>'+			      
		          '</tbody>'+
		          '</table>');
        table.find('caption').text(data.from+':'+data.to+':厨师关系');
        var rows = data.rows;
        for(var j in rows) {
            var one = rows[j];
            var tr = $('<tr>'+
			           '<td class="fid"></td>'+
                       '<td class="name">100</td>'+
                       '<td class="num">100</td>'+
			           '<td class="fb-num">1</td>'+
			           '<td class="good-num">98</td>'+
			           '<td class="normal-num">1</td>'+
			           '<td class="bad-num">1%</td>'+
                       '<td class="good-rate"></td>'+
                       '<td class="normal-rate"></td>'+
                       '<td class="bad-rate"></td>'+
			           '</tr>');
            tr.find('.fid').text(one.fid);
            tr.find('.name').text(one.name);
            tr.find('.num').text(one.num);
            tr.find('.fb-num').text(one['fb-num']);
            tr.find('.good-num').text(one['good-num']);
            tr.find('.normal-num').text(one['normal-num']);
            tr.find('.bad-num').text(one['bad-num']);
            tr.find('.good-rate').text(one['good-rate'].toFixed(2)+'%');
            tr.find('.normal-rate').text(one['normal-rate'].toFixed(2)+'%');
            tr.find('.bad-rate').text(one['bad-rate'].toFixed(2)+'%');
            table.find('tbody').append(tr);
            
        }
        p.append(table);

    }
}
