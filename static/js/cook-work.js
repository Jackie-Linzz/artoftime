$(document).ready(function(){

    //for mobile css
    if(/Android|webOS|iPhone|iPad|BlackBerry/i.test(navigator.userAgent)) {
    } else {
	    var css = $('#css').attr('href');
	    css = css.replace(/-mobile/g, '');
	    $('#css').attr('href', css);
    }
    window.cook = {};
    window.lock = false;


    $('.tab').hide();
    $('.doing').show();

    $(document).on('click', '#select', function(){
	    $('.tab').hide();
	    $('.select').show();
        
    });
    $(document).on('click', '#doing', function(){
	    $('.tab').hide();
	    $('.doing').show();
    });
    $(document).on('click', '#done', function(){
	    $('.tab').hide();
	    $('.done').show();
    });
    $(document).on('click', '.back', function(){
	    window.location.replace('/cook-home');
    });
    $(document).on('click', '.byway .item', function(){
	    $(this).toggleClass('selected');
    }); 
    
    //instructions
    $(document).on('click', '.refuse-button', function(){
	    var ins = ['refuse'];
	    $.postJSON(
	        '/cook-ins',
	        {'fid': window.cook.fid, 'ins': json(ins)},
	        function(){}
	    );
    });
    $(document).on('click', '.prepare-button', function(){
	    var ins = ['prepare'];
	    $.postJSON(
	        '/cook-ins',
	        {'fid': window.cook.fid, 'ins': json(ins)},
	        function(){}
	    );
    });
    $(document).on('click', '.accept-button', function(){
	    var ins = ['accept'];
        //ins.push($('.current').data('uid'));
	    /* $('.byway .selected').each(function(){
	       var uid = $(this).data('uid');
	       ins.push(uid);
	       });*/
	    $.postJSON(
	        '/cook-ins',
	        {'fid': window.cook.fid, 'ins': json(ins)},
	        function(){}
	    );
	    
    });

    $(document).on('click', '.byway .item .close', function(){
	    var uid = $(this).parent().data('uid');
	    var ins = ['cancel-byway', uid];
	    $.postJSON(
	        '/cook-ins',
	        {'fid': window.cook.fid, 'ins': json(ins)},
	        function(){}
	    );
    });
    $('.doing').on('click', '.close', function(){
	    var uid = $(this).parent().data('uid');
	    var ins = ['cancel-doing', uid];
	    $.postJSON(
	        '/cook-ins',
	        {'fid': window.cook.fid, 'ins': json(ins)},
	        function(){}
	    );
        /* var div = $('<div></div>');
         * div.text('doing,close,'+uid);
         * $('.debug').append(div);*/
    });
    /* $('.doing').on('click', '.finish', function(){
	   var uid = $(this).parent().data('uid');
	   var ins = ['done', uid];
     *     console.log('.doing .item .finish', ins);
	   $.postJSON(
	   '/cook-ins',
	   {'fid': window.cook.fid, 'ins': json(ins)},
	   function(){}
	   );
     * });*/
    $(document).on('click', '.do-all', function(){
        if(window.lock) return;
        window.lock = true;
        var ins = ['done-all'];
        $.postJSON(
	        '/cook-ins',
	        {'fid': window.cook.fid, 'ins': json(ins)},
	        function(){
                var ins = ['prepare'];
	            $.postJSON(
	                '/cook-ins',
	                {'fid': window.cook.fid, 'ins': json(ins)},
	                function(){
                        var ins = ['accept'];
                        $.postJSON(
	                        '/cook-ins',
	                        {'fid': window.cook.fid, 'ins': json(ins)},
	                        function(){}
	                    );
                    }
	            );
            }
	    );
        setTimeout(reset_lock, 1000*5);
    });
    updater.poll();
    left_updater.poll();
});
function reset_lock() {
    window.lock = false;
}
function show_select() {
    var current = window.cook.current;
    var byway = window.cook.byway;
    //show current
    if(current == '') {
	    $('.current').data('uid', '');
	    $('.current .title').text('');
	    $('.current .num').text('');
	    $('.current .desk').text('');
	    $('.current .demand').text('');
    } else {
	    $('.current').data('uid', current.uid);
	    $('.current .title').text(current.name);
	    $('.current .num').text(current.num);
	    $('.current .desk').text(current.desk);
	    $('.current .demand').text(current.demand+'|'+current.gdemand);
    }
    //show byway
    var p = $('.byway').empty();
    for(var i in byway) {
	    var one = byway[i];
	    var item = $('<div class="item">'+
		             '<div class="close">X</div>'+
		             '<div class="title"></div>'+
		             '<div class="info"><div class="num"></div>::<div class="desk"></div></div>'+
		             '<div class="demand"></div>'+
		             '</div>');
	    item.data(one);
	    item.find('.title').text(one.name);
	    item.find('.num').text(one.num);
	    item.find('.desk').text(one.desk);
	    item.find('.demand').text(one.demand+'|'+one.gdemand);
	    p.append(item);
    }

}
function show_doing() {
    var doing = window.cook.doing;
    $('.doing .item').remove();
    var p = $('.doing');
    for(var i in doing) {
	    var one = doing[i];
	    var item = $('<div class="item">'+
		             '<div class="close">X</div>'+
		             '<div class="title">宫保鸡丁</div>'+
		             '<div class="info"><div class="num">1</div>::<div class="desk">1</div></div>'+
		             '<div class="demand">不要辣</div>'+
		             //'<div class="finish">完成</div>'+
	                 '</div>');
	    item.data(one);
	    item.find('.title').text(one.name);
	    item.find('.num').text(one.num);
	    item.find('.desk').text(one.desk);
	    item.find('.demand').text(one.demand+'|'+one.gdemand);
	    p.append(item);
    }
}
function show_done() {
    var done = window.cook.done;
    var p = $('.done').empty();
    for(var i in done) {
	    var one = done[i];
	    var item = $('<div class="item">'+

		             '<div class="title">宫保鸡丁</div>'+
		             '<div class="info"><div class="num">1</div>::<div class="desk">1</div></div>'+
		             '<div class="demand">不要辣</div>'+
	                 '</div>');
	    item.data(one);
	    item.find('.title').text(one.name);
	    item.find('.num').text(one.num);
	    item.find('.desk').text(one.desk);
	    item.find('.demand').text(one.demand+'|'+one.gdemand);
	    p.append(item);
    }
}
function show_content(){
    show_select();
    show_doing();
    show_done();
}

var updater = {
    interval: 500,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){
	    var fid = getCookie('fid');
        console.log('polling', updater.cursor);
        updater.cursor += 1;
        updater.xhr = $.ajax({
            url: '/cook-work-update',
            type: 'POST',
            dataType: 'json',
            data: {'fid': fid, 'stamp': json(updater.stamp)},
            success: updater.onSuccess,
            error: updater.onError
        });

    },
    onSuccess: function(response){
        window.cook = response.cook;
        updater.stamp = cook.stamp;
        show_content();
        updater.interval = 500;
        setTimeout(updater.poll, updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        updater.interval = updater.interval*2;
        setTimeout(updater.poll, updater.interval);
    },
    reset: function(){
        updater.stamp = 0;
        updater.cursor = 0;
        updater.interval = 800;
        updater.xhr.abort();
    }
};
function show_left() {
    $('.left').text(window.left);
}
var left_updater = {
    interval: 500,
    stamp: 0,
    cursor: 0,
    xhr: null,
    poll: function(){

        console.log('polling', left_updater.cursor);
        left_updater.cursor += 1;
        left_updater.xhr = $.ajax({
            url: '/cook-left-update',
            type: 'POST',
            dataType: 'json',
            data: {'stamp': json(left_updater.stamp)},
            success: left_updater.onSuccess,
            error: left_updater.onError
        });

    },
    onSuccess: function(response){
        window.left = response.left;
        left_updater.stamp = response.stamp;
        show_left();
        left_updater.interval = 500;
        setTimeout(left_updater.poll, left_updater.interval);
    },
    onError: function(response, error) {
        console.log(error);
        left_updater.interval = left_updater.interval*2;
        setTimeout(left_updater.poll, left_updater.interval);
    },
    reset: function(){
        left_updater.stamp = 0;
        left_updater.cursor = 0;
        left_updater.interval = 800;
        left_updater.xhr.abort();
    }
};
