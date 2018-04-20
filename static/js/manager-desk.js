$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $('.tab').hide();
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '.menu .add', function(){
	    $('.tab').hide();
	    $('.desk-add').show();
    });
    $(document).on('click', '.menu .del', function(){
	    $('.tab').hide();
	    $('.desk-del').show();
    });
    $(document).on('click', '.menu .show', function(){
	    $('.tab').hide();
	    $('.desk-show').show();
	    $.postJSON(
	        '/manager-desk-show',
	        {},
	        function(response){
		        if(response.status != 'ok') return;
		        var desks = response.desks;
		        var p = $('.desk-show tbody').empty();
		        for(var i in desks) {
		            if(i % 5 == 0) {
			            var tr = $('<tr></tr>');
			            p.append(tr);
		            }
		            var td = $('<td></td>');
		            td.text(desks[i].desk+'('+desks[i].num+')');
		            tr.append(td);
		        }
	        }
	    );
    });
    $(document).on('click', '#desk-add-button', function(){
	    var desk = $('#desk-add').val();
	    desk = trim(desk);
        var seats = $('#desk-seats').val();
        seats = trim(seats);
	    if(desk == '') return;
        if(seats == '') return;
	    $.postJSON(
	        '/manager-desk-add',
	        {'desk': desk, 'seats': seats},
	        function(response) {
		        if(response.status == 'ok') {
		            $('#desk-add').val('');
                    $('#desk-seats').val('');
		        }
	        }
	    );
    });
    $(document).on('click', '#desk-del-button', function(){
	    var desk = $('#desk-del').val();
	    desk = trim(desk);
	    if(desk == '') return;
	    $.postJSON(
	        '/manager-desk-del',
	        {'desk': desk},
	        function(response) {
		        if(response.status == 'ok') {
		            $('#desk-del').val('');
		        }
	        }
	    );
    });
});
