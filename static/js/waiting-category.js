$(document).ready(function(){
    $(document).on('tap', '.item', function(e){
	var cid = $(this).attr('data-cid');
	window.location.replace('/waiting-diet?cid='+cid);
    });
    $(document).on('tap', '.footer', function(e){
	window.location.replace('/waiting-order');
    });
});

