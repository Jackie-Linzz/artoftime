$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $(document).on('tap', '.button', function(e){
	    var number = $('.number').val();
        console.log(typeof number);
	    number = trim(number);
	    if(number == '') return;
	    $.postJSON(
	        '/waiting-entry',
	        {'number': number},
	        function(response){
		        if(response.status == 'ok'){
		            window.location.replace('/waiting-queue');
		        }
	        }
	    );
    });
});
