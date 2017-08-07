$(document).ready(function(){
    $(document).on('tap', '.button', function(e){
	var number = $('.number').val();
	number = trim(number);
	if(number == '') return;
	$.postJSON(
	    '/waiting-entry',
	    {'number': number},
	    function(response){
		if(response.status == 'ok'){
		    window.location.replace('/waiting-category');
		}
	    }
	);
    });
});
