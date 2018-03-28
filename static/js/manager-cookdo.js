$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $('.result2').hide();
    window.faculty = [];
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
    $('#fid').val('all');
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('change', 'select', function(){
        var fid = $(this).val();
        $('#fid').val(fid);
    });
    $(document).on('click', '#cookdo-button', function(){
	    $('.result2').hide();

	    var fid = $('#fid').val();
	    fid = trim(fid);
	    if(fid == '') return;
	    $.postJSON(
	        '/manager-cookdo',
	        {'fid': fid},
	        function(response) {
		        if(response.status == 'ok') {
                    var result = response.result;
                    var p = $('.result').empty();
                    for(var i in result) {
                        var one = result[i];
                        var table = $('<table border="1" cellspacing="0" class="result2">'+
		                              '<caption>工号：名字</caption>'+
		                              '<thead>'+
			                          '<tr><th>编号</th><th>名称</th><th>分组</th></tr>'+
		                              '</thead>'+
		                              '<tbody></tbody>'+
		                              '</table>');
                        table.find('caption').text(one.fid+':'+one.name);
                        var diet = one.diet;
                        for(var j in diet){
                            var one_diet = diet[j];
                            var tr = $('<tr><td class="did"></td><td class="name"></td><td class="cid"></td></tr>');
                            tr.find('.did').text(one_diet.did);
                            tr.find('.name').text(one_diet.name);
                            tr.find('.cid').text(one_diet.cid);
                            table.append(tr);
                        }
                        p.append(table);
                    }

		        }
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
