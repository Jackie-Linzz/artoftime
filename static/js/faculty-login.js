$(document).ready(function(){
    $(document).on('tap', '.confirm', function(){
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
    $(document).on('tap', '.back', function(){
	window.location.replace('/');
    });
});
