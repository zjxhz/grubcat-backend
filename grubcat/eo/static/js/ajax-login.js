function ajaxLoginRequire(responseData, callBackAfterLogined, callBackIfLogined){
    //if(responseData.needLogin){
    if(true){
        showLoginDialog(callBackAfterLogined);
    } else {
        callBackIfLogined();
    }
}

function showLoginDialog(callBackAfterLogined) {
    $("<div id='login_dialog' style='display:none'></div>").load('/user/login', function(){
        $("#login_form").ajaxForm({
            success:function (html) {
                try {
                    callBackAfterLogined();
                }catch(e){}
            }
        })
        $(this).dialog({
            autoOpen:true,
            title:"登录",
            modal:true,
            width:440,
            height:360,
            position:['center', 100],
            resizable:false
        });
    })
}
