$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $(document).on('click', '.item', function(e){
	    var cid = $(this).attr('data-cid');
	    window.location.replace('/waiting-diet?cid='+cid);
    });
    $(document).on('click', '.footer', function(e){
	    window.location.replace('/waiting-order');
    });
});
