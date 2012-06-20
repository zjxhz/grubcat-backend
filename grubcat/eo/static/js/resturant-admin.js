$(document).ready(function () {

    var options = {
        target:        '#result'   // target element(s) to be updated with server response
//        beforeSubmit:  showRequest,  // pre-submit callback
//        success:       showResponse  // post-submit callback
    };
    // bind form using 'ajaxForm'
    $('#checkin-form').ajaxForm(options);
})


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
function showResponse(responseText, statusText, xhr, $form)  {
    alert('status: ' + statusText + '\n\nresponseText: \n' + responseText +
        '\n\nThe output div should have already been updated with the responseText.');
}