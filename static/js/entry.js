$(document).ready(function(){
    $(document).on('tap', '.button', function(e){
	var desk = $('.desk').val();
	desk = trim(desk);
	$.postJSON(
	    '/',
	    {'desk': desk},
	    function(response){
		if(response.status == 'ok') {
		    window.location.replace('/customer-home?desk='+desk.toUpperCase());
		}
	    }
	);
    });
    $(document).on('taphold', '.header', function(){
	window.location.replace('/faculty-login');
    });
});
