$(document).ready(function ($) {

    $("#main-nav ul.nav li").removeClass("active");
    var $active = $("#" + $("#data").data('navActiveId'))
    $active.addClass("active");
    $("#main-nav ul.nav  li").not(".active").hover(function () {
        $active.removeClass("active");
        $(this).addClass("active");
    }, function () {
        $(this).removeClass("active");
        $active.addClass("active");
    });

    var $commentContainer = $("#comment-container")
    if ($commentContainer[0]){

        $commentContainer.find(".comment").hover(function(){
            $(this).find(".comment-time, .comment-footer").css('visibility', 'visible')
        }, function(){
            $(this).find(".comment-footer").css('visibility', 'hidden')
        })

    }

})