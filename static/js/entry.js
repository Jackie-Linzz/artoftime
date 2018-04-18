$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $(document).on('click', '.button', function(e){
	    var desk = $('.desk').val();
	    desk = trim(desk);
        //alert(desk);
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
    $(document).on('click', '.header', function(){
	    window.location.replace('/faculty-login');
    });
});
