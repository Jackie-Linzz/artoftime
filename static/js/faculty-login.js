$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $(document).on('click', '.confirm', function(){
	    var fid = $('#fid').val();
	    var passwd = $('#passwd').val();
	    fid = trim(fid);
	    passwd = trim(passwd);
	    $.postJSON(
	        '/faculty-login',
	        {'fid': fid, 'passwd': passwd},
	        function(response){
		        //console.log('response');
		        if(response.status == 'ok') {
		            //console.log('ok');
		            window.location.replace('/faculty-role');
		        }
	        }
	    );
    });
    $(document).on('click', '.back', function(){
	    window.location.replace('/');
    });
});
