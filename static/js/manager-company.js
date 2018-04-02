$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }

    $.postJSON(
	    '/manager-company',
	    {},
	    function(response){
	        info = response.info;
	        $('#company').val(info.company);
	        $('#shop').val(info.shop);
	        $('#location').val(info.location);
            $('#time').val(info.time);
	        $('#heading').val(info.heading);
	        $('#welcome').val(info.welcome);
	        $('#desp').val(info.desp);
	    }
    );

    $(document).on('click', '.button', function(){
	    var company = trim($('#company').val());
	    var shop = trim($('#shop').val());
	    var location = trim($('#location').val());
        var time = trim($('#time').val());
	    var heading = trim($('#heading').val());
	    var welcome = trim($('#welcome').val());
	    var desp = trim($('#desp').val());
	    $.postJSON(
	        '/manager-company-set',
	        {'company': company, 'shop': shop, 'location': location, 'time': time, 'heading': heading, 'welcome': welcome, 'desp': desp},
	        function(response){
		        if(response.status == 'ok') {
		        } else {
		            $('#company').val('');
		            $('#shop').val('');
		            $('#location').val('');
                    $('#time').val('');
		            $('#heading').val('');
		            $('#welcome').val('');
		            $('#desp').val('');
		        }
	        }
	    );
    });
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
});
