$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $('.result1').hide();
    $('.result2').hide();
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    $(document).on('click', '#cookdo-button', function(){
	    $('.result1').hide();
	    $('.result2').hide();

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
