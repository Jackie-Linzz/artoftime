$(document).ready(function(){
    $('.tab').hide();
    $(document).on('tap', '.menu .add', function(){
	$('.tab').hide();
	$('.desk-add').show();
    });
    $(document).on('tap', '.menu .del', function(){
	$('.tab').hide();
	$('.desk-del').show();
    });
    $(document).on('tap', '.menu .show', function(){
	$('.tab').hide();
	$('.desk-show').show();
	$.postJSON(
	    '/manager-desk-show',
	    {},
	    function(response){
		if(response.status != 'ok') return;
		var desks = response.desks;
		var p = $('.desk-show tbody').empty();
		for(var i in desks) {
		    if(i % 5 == 0) {
			
		    }
		}
	    }
	);
    });
    $(document).on('tap', '#desk-add-button', function(){
	var desk = $('#desk-add').val();
	desk = trim(desk);
	if(desk == '') return;
	$.postJSON(
	    '/manager-desk-add',
	    {'desk': desk},
	    function(response) {
		if(response.status == 'ok') {
		    $('#desk-add').val('');
		}
	    }
	);
    });
    $(document).on('tap', '#desk-del-button', function(){
	var desk = $('#desk-del').val();
	desk = trim(desk);
	if(desk == '') return;
	$.postJSON(
	    '/manager-desk-del',
	    {'desk': desk},
	    function(response) {
		if(response.status == 'ok') {
		    $('#desk-add').val('');
		}
	    }
	);
    });
});
