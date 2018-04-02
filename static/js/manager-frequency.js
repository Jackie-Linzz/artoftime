$(document).ready(function(){
    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.tables = [];
    $('.result').empty();
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '.button', function(){
        $('.result').hide();
        var date = $('#date').val();
        var request = $('#request').prop('checked');
        var kitchen = $('#kitchen').prop('checked');
        var cash = $('#cash').prop('checked');

        console.log(date);

        if(date == '') return;
        if((request || kitchen || cash) == false) return;

        if(request) request = 1;
        else request = 0;

        if(kitchen) kitchen = 1;
        else kitchen = 0;

        if(cash) cash = 1;
        else cash = 0;

        $.postJSON(
            '/manager-frequency',
            {'date': date, 'request': request, 'kitchen': kitchen, 'cash': cash},
            function(response) {
                window.tables = response.result;
                show_tables();
                $('.result').show();
            }
        );
    });
});
function show_tables(){
    var p = $('.result').empty();
    for(var i in window.tables) {
        var table = window.tables[i];
        console.log(table);
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
