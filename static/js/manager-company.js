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
	        $('#heading').val(info.heading);
	        $('#welcome').val(info.welcome);
	        $('#desp').val(info.desp);
	    }
    );

    $(document).on('tap', '.button', function(){
	    var company = $('#company').val();
	    var shop = $('#shop').val();
	    var location = $('#location').val();
	    var heading = $('#heading').val();
	    var welcome = $('#welcome').val();
	    var desp = $('#desp').val();
	    $.postJSON(
	        '/manager-company-set',
	        {'company': company, 'shop': shop, 'location': location, 'heading': heading, 'welcome': welcome, 'desp': desp},
	        function(response){
		        if(response.status == 'ok') {
		        } else {
		            $('#company').val('');
		            $('#shop').val('');
		            $('#location').val('');
		            $('#heading').val('');
		            $('#welcome').val('');
		            $('#desp').val('');
		        }
	        }
	    );
    });
    $(document).on('tap', '.back', function(){
	    window.location.replace('/manager-home');
    });
});
