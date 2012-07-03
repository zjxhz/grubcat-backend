$(document).ready(function () {

    $("#restaurant-nav li").removeClass("active");
    $("#" + $("#nav-active-id").html()).addClass("active")

    $("a.dellink").click(function () {
        var $link = $(this);
        var href = $link.attr('href');
        $.fn.dialog2.helpers.confirm("确定要删除这道菜吗？", {
            title:'确认',
            confirm:function () {
                $.post(href, function () {
                    $link.parents("tr").fadeOut(300);
                })
            }
        });
        return false;
    });

    // bind form using 'ajaxForm'
    $('#checkin-form').ajaxForm({target:'#result' });

    $("#modal-dialog").live("dialog2.content-update", function (e, data) {
        // got the dialog as this object. Do something with it!
        var e = $(this);
        var autoclose = e.find("a.auto-close");
        if (autoclose.length > 0) {
            e.dialog2('close');
            var href = autoclose.attr('href');
            if (href) {
                window.location.href = href;
            }
        }
    });
});


// pre-submit callback
function showRequest(formData, jqForm, options) {
    // formData is an array; here we use $.param to convert it to a string to display it
    // but the form plugin does this for you automatically when it submits the data
    var queryString = $.param(formData);

    alert('About to submit: \n\n' + queryString);

//    $("#result").html("")
    return true;
}

// post-submit callback
function showResponse(responseText, statusText, xhr, $form) {
    alert('status: ' + statusText + '\n\nresponseText: \n' + responseText +
        '\n\nThe output div should have already been updated with the responseText.');
}