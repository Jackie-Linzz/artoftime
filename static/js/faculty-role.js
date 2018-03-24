$(document).ready(function(){
    //alert(navigator.userAgent);
    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $(document).on('click', '.logout', function(){
	    window.location.replace('/faculty-login');
    });
    $(document).on('click', '.manager', function(){
	    $.postJSON(
	        'faculty-role',
	        {'role': 'manager'},
	        function(response){
		        if(response.status == 'ok') window.location.replace('/manager-home');
	        }
	    );
    });
    $(document).on('click', '.waiter', function(){
	    $.postJSON(
	        'faculty-role',
	        {'role': 'waiter'},
	        function(response){
		        if(response.status == 'ok') window.location.replace('/waiter-home');
	        }
	    );
    });
    $(document).on('click', '.cashier', function(){
	    $.postJSON(
	        'faculty-role',
	        {'role': 'cashier'},
	        function(response){
		        if(response.status == 'ok') window.location.replace('/cashier-home');
	        }
	    );
    });
    $(document).on('click', '.cook', function(){
	    $.postJSON(
	        'faculty-role',
	        {'role': 'cook'},
	        function(response){
		        if(response.status == 'ok') window.location.replace('/cook-home');
	        }
	    );
    });
});
