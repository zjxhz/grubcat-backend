function scrollToElement($element, speed, offset) {
    speed=speed||1000
    offset=offset||40
    if ($element.length)
        $("html,body").animate({scrollTop: $element.offset().top - (offset || 0) }, speed || 1000);
}

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
    if ($commentContainer[0]) {
        $commentContainer.load($commentContainer.data("comment-list-url"))
        $commentContainer.on('mouseenter', ".comment",function () {

            $(this).find(".comment-actions").show()

        }).on('mouseleave', ".comment",function () {

                $(this).find(".comment-actions").hide()

            }).on('click', ".btn-submit-comment",function () {

                var $commentForm = $(this).parents("form"), $parent = $commentForm.find('[name=parent]'),
                    $comment = $commentForm.find('[name=comment]')
                if(!$comment.val() || !$comment.val().trim() ){
                    $comment.focus()
                    return false
                }

                $.post($commentForm.attr('action'), {
                    'parent': $parent.val(),
                    'comment': $comment.val()
                }, function (data) {
                    if (data.status == 'OK') {
                        var $newComment = $(data.html)
                        $newComment.hide().insertBefore($("#comment_box")).slideDown()
                        scrollToElement($newComment,500)
                        $("#reply_box").hide()
                    } else {
                        alert('评论没有成功！' + data.comment)
                    }
                    $comment.val('')
                    $parent.val('')
                })

                return false

            }).on('click', '.reply-link', function(){

                var $replyBox = $("#reply_box")
                $replyBox.appendTo($(this).parents(".comment-body")).show()

                var parentId = $(this).parents(".comment").attr("id").replace('comment-','')
                $replyBox.find('[name=parent]').val(parentId)
                $replyBox.find("[name=comment]").val('').focus()

//                scrollToElement($("#comment_form"))
//                $("#id_comment").focus()
                return false;

            }).on('keydown', '[name=comment]', function(e){

                if (e.ctrlKey && e.keyCode == 13) {
                   $(this).siblings(".btn-submit-comment").click()
                }

            })
    }

})