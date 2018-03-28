$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.tables = [];
    $(document).on('click', '.back', function(){
	    window.location.replace('/manager-home');
    });
    
    
    $(document).on('click', '#flow-query', function(){
	    $('.flow-content').hide();

	    var from = $('#flow-from').val();
	    var to = $('#flow-to').val();
        var trend = $('#trend').prop('checked');

	    from = trim(from);
	    to = trim(to);

	    if(from == '') return;
	    if(to == '') return;

        if(trend){
            trend = 1;
        } else {
            trend = 0;
        }

	    $.postJSON(
	        '/manager-history-flow',
	        {'from': from, 'to': to, 'trend': trend},
	        function(response) {
		        if(response.status != 'ok') return;
		        $('.flow-content').show();
		        window.tables = response.result;
		        //console.log(flow);
		        show_tables();
	        }
	    );
    });
    
    
});

function show_tables(){
    
}
