$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.cookdo = [];
    $.postJSON(
	    '/cook-do',
	    {},
	    function(response) {
	        if(response.status != 'ok') return;
	        window.cookdo = response.cookdo;
	        show();
	    }
    );
    $(document).on('click', '.back', function(){
	    window.location.replace('/cook-home');
    });
    $(document).on('click', '#submit1', function(){
	    var flag = $('.all input').prop('checked');
	    if(flag == true) {
	        var content = ['all'];
	        $.postJSON(
		        '/cook-do-submit',
		        {'content': json(content)},
		        function(response) {
		            if(response.status != 'ok') return;
		            window.cookdo = response.cookdo;
		            show();
		        }
	        );
	    }
    });
    $(document).on('click', '#submit2', function(){
	    var content = [];
	    $('.some input:checkbox:checked').each(function(){
	        var did = $(this).parents('tr').data('did');
	        content.push(did);
	    });
	    $.postJSON(
	        '/cook-do-submit',
	        {'content': json(content)},
	        function(response) {
		        if(response.status != 'ok') return;
		        window.cookdo = response.cookdo;
		        show();
	        }
	    );
    });
});
function show() {
    var content = window.cookdo;
    if(content.length == 0) {
	    $('input:checkbox').attr('checked', false);
	    return;
    }
    if(content[0] == 'all') {
	    $('.all input:checkbox').attr('checked', true);
	    $('.some input:checkbox').attr('checked', false);
	    return;
    } else {
	    $('.all input:checkbox').attr('checked', false);
	    $('.some input:checkbox').each(function(){
	        var did = $(this).parents('tr').data('did');
	        var flag = false;
	        for(var i in content) {
		        if(did == content[i]) {
		            flag = true;
		            break;
		        }
	        }
	        $(this).attr('checked', flag);
	    });
    }

}
