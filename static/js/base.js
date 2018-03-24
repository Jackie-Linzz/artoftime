function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
function setCookie(cname,cvalue,exdays)
{
    var d = new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}


$.postJSON = function(url, args, callback) {
   // console.log(args);
    $.ajax(
        {
            url: url,
            data: args,
            dataType: "json",
            type: "POST",
            success: function(response) {
                if (callback) callback(response);
            },
            error: function(response) {
                console.log("ERROR:", response);
            }
        }
    );
};


var json = JSON.stringify;


var delay = 5000;
var disablebutton = function(b$){
    b$.attr('disabled', true);
    setTimeout(function(){
        b$.attr('disabled', false);
    }, 5000);
};
var disable = function(b$, delay) {

};

function trim(str) {
    return str.replace(/(^\s*)|(\s*$)/g,'');
}

