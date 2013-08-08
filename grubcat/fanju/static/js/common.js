function scrollToElement($element, speed, offset) {
    if ($element.length)
        $("html,body").animate({scrollTop: $element.offset().top - (offset || 0) }, speed || 1000);
}

$(document).ready(function ($) {

    var $commonData = $("#common-data")
    var isLogined = $commonData.data("uid") != ""

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
        $.get($commentContainer.data("comment-list-url"), function(data){
            var $comments = $(data)
            var viewerId = $comments.find("#comment_box").data('uid'),
                vieweeId = $("#data").data('ownerId'), commentOwnerId

            $comments.find(".comment").each(function () {
                commentOwnerId = $(this).data('uid')
                if (viewerId == commentOwnerId) {
                    $(this).find(".comment-actions").append('<a href="#" class="del-comment-link"></i>删除</a>')
                }
                if (vieweeId == commentOwnerId) {
                    $(this).addClass('viewee')
                }
            })
            $commentContainer.html($comments)
            if (location.hash.indexOf('#comment-') > -1) {
                var $commentToGo = $(location.hash)
                if ($commentToGo[0]) {

                    scrollToElement($commentToGo)
                    $commentToGo.css('background-color', '#ffc40d').animate({"background-color": "#FFF"}, 3000)
                } else {
                    noty({text: "评论已经被用户删除", timeout: 2000, type:'warning'});
                }
            }
        })
        $commentContainer.on('mouseenter', ".comment",function () {

            $(this).find(".comment-actions").show()

        }).on('mouseleave', ".comment",function () {

                $(this).find(".comment-actions").hide()

            }).on('click', ".btn-submit-comment",function () {

                var $commentForm = $(this).parents("form"), $parent = $commentForm.find('[name=parent]'),
                    $comment = $commentForm.find('[name=comment]'), comment = $comment.val()
                if(!comment|| !comment.trim() ){
                    $comment.focus()
                    return false
                }
                if(comment.length > 200){
                    alert('最多只能输入200字，已经超出' + (comment.length-200) + '字')
                    $comment.focus()
                    return false
                }
                var $btnSubmit = $commentForm.find("button.btn-submit-comment")
                    $btnSubmit.attr('disabled',true).addClass('disabled')
                $.post($commentForm.attr('action'), {
                    'parent': $parent.val(),
                    'comment': $comment.val()
                }, function (data) {
                    if (data.status == 'OK') {
                        $btnSubmit.removeAttr('disabled').removeClass('disabled')
                        var $newComment = $(data.html), viewerId = $("#comment_box").data('uid'), vieweeId = $("#data").data('ownerId')
                        if (viewerId && $newComment.data('uid') == viewerId) {
                            $newComment.find(".comment-actions").append('<a href="#" class="del-comment-link"></i>删除</a>')
                        }
                        if (vieweeId == $newComment.data('uid')) {
                            $newComment.addClass('viewee')
                        }

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

            }).on('click', '.del-comment-link', function(){

                var $commentToDel =  $(this).parents(".comment")
                var commentId = $commentToDel.attr('id').replace("comment-",'')
                var delCommentUrl = $commentContainer.data('delCommentUrl').replace('1',commentId )

                $commentToDel.find("#reply_box").hide().insertBefore("#comment_box")

                $.post(delCommentUrl, function(){
                    $commentToDel.slideUp(function(){
                        $commentToDel.remove()
                    })
                })
                return false

            }).on('keydown', '[name=comment]', function(e){

                if (e.ctrlKey && e.keyCode == 13) {
                   $(this).siblings(".btn-submit-comment").click()
                }

            }).on('focus', '[name=comment]', function(){
                $(this).siblings('.btn-submit-comment').css('display','block')
            })
    }

    var $likeLink = $("#like-link"), $mealDetailPage = $("#meal-detail-page")
    if($likeLink[0] ){
        var orginalLikeLink = $likeLink.html(), isAlreadyLiked = $likeLink.data("isAlreadyLiked"),
            likeText = $likeLink.data("likeText") || "赞"


        $likeLink.hover(function () {
            if (isAlreadyLiked) {
                $likeLink.html("&nbsp;已" + likeText)
            }
        }, function () {
            $likeLink.html(orginalLikeLink)
        })

        $likeLink.click(function () {
            if (isAlreadyLiked)
                return false
            $.post($likeLink.attr("href"), function (data) {
                if (!data.already_liked) {
                    var $likeNum = $("#like-wrapper .like-num")
                    $likeNum.text(parseInt($likeNum.text()) + 1)
                }
                isAlreadyLiked = true
            })

            return false
        })

    } else if($likeLink[0]){
        $likeLink.click(function(){
            $.post($likeLink.attr("href"), function(data){
                var alreadyLiked = data.already_liked
                if (alreadyLiked) {
                    noty({text: '你对我们这个饭局很感兴趣啊，</br>不妨来参加下，大家一起交个朋友！', timeout: 3000})
                } else {
                    var $likeNum = $("#like-wrapper .like-num")
                    $likeNum.text(parseInt($likeNum.text()) + 1)
                }
            })

            return false
        })
    }

    $(".need-login").click(function(){

        if(!isLogined){
            var loginBackUrl = $(this).data("login-back-url") || $(this).attr("href")
            window.location = "/login/weibo/?next=" + loginBackUrl
        }
    })

})