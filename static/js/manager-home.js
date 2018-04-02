$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    $(document).on('click', '.back', function(){
	    window.location.replace('/faculty-role');
    });
    $(document).on('click', '.company', function(){
	    window.location.replace('/manager-company');
    });
    $(document).on('click', '.diet', function(){
	    window.location.replace('/manager-diet');
    });
    $(document).on('click', '.desk', function(){
	    window.location.replace('/manager-desk');
    });
    $(document).on('click', '.order', function(){
        window.location.replace('/manager-order');
    });
    $(document).on('click', '.faculty', function(){
	    window.location.replace('/manager-worker');
    });
    $(document).on('click', '.cookdo', function(){
	    window.location.replace('/manager-cookdo');
    });
    $(document).on('click', '.today', function(){
        window.location.replace('/manager-today');
    });
    $(document).on('click', '.achievement', function(){
	    window.location.replace('/manager-achievement');
    });
    $(document).on('click', '.flow', function(){
	    window.location.replace('/manager-history');
    });
    $(document).on('click', '.one-diet', function(){
        window.location.replace('/manager-onediet');
    });
    $(document).on('click', '.frequency', function(){
        window.location.replace('/manager-frequency');
    });
    $(document).on('click', '.comment', function(){
	    window.location.replace('/manager-comment');
    });
    $(document).on('click', '.mask', function(){
	    window.location.replace('/manager-mask');
    });
    $(document).on('click', '.passwd', function(){
	    window.location.replace('/faculty-secret?back=manager-home');
    });
    $(document).on('click', '.shutdown', function(){
	    window.location.replace('/manager-shutdown');
    });
});
