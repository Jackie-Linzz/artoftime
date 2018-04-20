$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    var order = getCookie('order')
    $('.order').text(order);
    $(document).on('tap', '.button', function(e){
	    window.location.replace('/waiting-entry');
    });
});
