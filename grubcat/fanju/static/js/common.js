$(document).ready(function ($) {

    $("#main-nav ul.nav li").removeClass("active");
    var $active = $("#" + $("#nav-active-id").html());
    $active.addClass("active");
    $("#main-nav ul.nav  li").not(".active").hover(function () {
        $active.removeClass("active");
        $(this).addClass("active");
    }, function () {
        $(this).removeClass("active");
        $active.addClass("active");
    });
})