$(document).ready(function(){
    $(document).on('tap', '.manager', function(){
	$.postJSON(
	    'faculty-role',
	    {'role': 'manager'},
	    function(response){
		if(response.status == 'ok') window.location.replace('/manager-home');
	    }
	);
    });
    $(document).on('tap', '.waiter', function(){
	$.postJSON(
	    'faculty-role',
	    {'role': 'waiter'},
	    function(response){
		if(response.status == 'ok') window.location.replace('/waiter-home');
	    }
	);
    });
    $(document).on('tap', '.cashier', function(){
	$.postJSON(
	    'faculty-role',
	    {'role': 'cashier'},
	    function(response){
		if(response.status == 'ok') window.location.replace('/cashier-home');
	    }
	);
    });
    $(document).on('tap', '.cook', function(){
	$.postJSON(
	    'faculty-role',
	    {'role': 'cook'},
	    function(response){
		if(response.status == 'ok') window.location.replace('/cook-home');
	    }
	);
    });
});
