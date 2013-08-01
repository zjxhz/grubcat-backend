jQuery(function($){

    var $data = $("#data");



    $("#chat-dialog").on("show",function(){
        $("html").addClass("chat-app")
        if ($("body").height() > $(window).height()) {
            $("html").addClass("scroll")
        }
    }).on("hidden",function(e){
            setTimeout(function () {
                // a hack to prevent event loop for ever
                $("html").removeClass("chat-app scroll")
            },100)
        })

    if ($("#upload-photo-page")[0]) {
        $("#id_photo").change(function () {
            $("#id_upload_photo_form").ajaxSubmit({
                beforeSubmit: function () {
                    $(".loading").show();
                },
                success: function (data) {
                    data = $.parseJSON(data);
                    if (data.status == 'OK') {
                        window.location = data.redirect_url;
                        $(".loading").hide();
                    }
                }
            })
        })
    }

    $(".del-photo-link").click(function () {
        $.post($(this).attr('href'), function (data) {
            if (data.status = "OK") {
                window.location = data.redirect_url
            }
        });
        return false;
    });

    if($("#photo-list-page")[0]){
        $(".photo-request a").click(function(){
            $.post($(this).attr('href'), function(){
                noty({text:'成功发送求照片请求！', timeout:1000})
            })
            return false;
        })
    }

    if ($("#photo-detail-page")[0]) {

        var $photo = $("#photo-wrapper");
        var $nextPhoto = $(".photo-next");
        var $prevPhoto = $(".photo-prev");
//    if($photo.find('a').attr('href') != $nextPhoto.attr('url')){
        $photo.click(function (e) {
            if (e.clientX - $(this).offset().left < $(this).width() / 2) {
                $prevPhoto.addClass('highlight');
                $nextPhoto.removeClass('highlight');
            } else if (e.clientX - $(this).offset().left <= $(this).width()) {
                $nextPhoto.addClass('highlight');
                $prevPhoto.removeClass('highlight');
            }
            window.location = $(".highlight").attr('url');
            return false;
        }).hover(function () {
                $photo.addClass('photo-direction-active')
            },function () {
                $photo.removeClass('photo-direction-active')
            }).mousemove(function (e) {
                if (e.clientX - $(this).offset().left < $(this).width() / 2) {
                    $prevPhoto.addClass('highlight');
                    $nextPhoto.removeClass('highlight');
                } else if (e.clientX - $(this).offset().left <= $(this).width()) {
                    $nextPhoto.addClass('highlight');
                    $prevPhoto.removeClass('highlight');
                }
            });
//    } else{
//        $photo.click(function (e) {return false;}).style.cursor  ='none'
//    }
    }
    var $faq = $("#faq");
    if ($faq[0]) {
        $faq.find(".sidebar-box-content a").click(function () {
            var $next = $(this).next("p");
            var speed = 200;
            if ($next.is(":visible")) {
                $(this).next("p").slideUp(speed);
            } else {
                $(this).siblings("p:visible").slideUp(speed);
                $(this).next("p").slideDown(speed);
            }
        })
    }

    if ($("#meal-list")[0]) {
        $("img.lazy").lazyload({ threshold: 200, effect: 'fadeIn' });
        $("#restaurant-login-link").show()
    }

    if ($("#meal-detail")[0]) {
        var $num_persons = $("#id_num_persons");
        var leftPersons = $("#left_persons_tip").data('leftPersons');
        $num_persons.find("option:gt(" + (leftPersons - 1) + ")").remove();
        $num_persons.change(function () {
            $("#total_price").html($("#meal_price").text() * 100 * $(this).val() / 100);
        });
        var orginalOrderNumPersons = $data.data("num-persons")
        if (orginalOrderNumPersons){
            $num_persons.val(orginalOrderNumPersons);
            $("#meal-grub").find(".btn-book-now").text("去支付");
        }
        var orderTimeOut;
        $(".btn-book-now").click(function () {
            $("#order_info_form").submit();
//            $("#pay_result_dialog").modal({backdrop:'static'});
//            $("#meal-grub").find(".btn-book-now").text("支付中");
            if (!orderTimeOut) {
                orderTimeOut = setTimeout(function () {
                    setInterval(function () {
                        $.post($data.data("check-order-status-link"), function (data) {
                            if (data.status == "OK") {
                                location.reload();
                            }
                        })
                    }, 2000)
                }, 5000)
            }
            return false;
        });

        $(".user-img-wrapper, #like-link, .like-num").tooltip({'placement': 'bottom'});

    }

    if ($(".profile-page")[0]) {

        $("#profile-nav").find("li.active").removeClass("active");
        $("#" + $data.data("activeNavId")).addClass("active");

        $("#profile_actions .btn-follow, #profile_actions .btn-unfollow").live('click', function () {
            var $btn = $(this);
            $.post($(this).attr('href'), function (data) {
                if (data.status == "OK") {
                    $btn.replaceWith(data.html)
                } else {
                    setTimeout(function () {
                        self.location.reload();
                    }, 1000);
                }
            });
            return false;
        });
    }

    $(".btn-follow").live('click', function(){

        $("#data").data("follow-request", true)
        chatApp.connect()
    })


    var $followListPage = $("#follow-list-page");
    if ($followListPage[0]) {
        $followListPage.find(".btn-unfollow").live('click', function () {
            var $btn = $(this);
            $.post($(this).attr('href'), function () {
                $btn.parents(".following-cell").remove();
            });
            return false;
        })
    }

    if ($("#edit-profile-page")[0] || $("#bind-profile-page")[0]) {
        $("#profile-nav-info").addClass("active");

        var $originalTagInput = $("#id_tags");
        var user_tags = $originalTagInput.val();

        function selectionRemoved($item) {
            $item.find("a").remove();
            var tagValue;
            $(".hot-tags li").each(function (i, tag) {
                tagValue = $(this).text().replace('+ ', '');
                if (tagValue == $item.text().replace(/\s+/g, "")) {
                    $(tag).removeClass("selected");
                }

            })
            $item.remove();
        }

        $originalTagInput.autoSuggest($data.attr('list-tags-url'), {
            asHtmlID: 'tags',
            preFill: user_tags,
            keyDelay: 100,
            neverSubmit: true,
            startText: '',
            selectionRemoved: selectionRemoved
        });

        var $tagsValues = $("#as-values-tags");
        $tagsValues.attr('required', '').attr('data-validation-required-message',
            '请至少输入3个兴趣标签，这样会让别人更加了解你哦！');
        $("input,select,textarea").not("[type=submit]").jqBootstrapValidation();

        $('#tags').parents().find('form').submit(function () {

            var $valuesTags = $("#as-values-tags");
            var e = jQuery.Event("keydown");//模拟一个键盘事件
            e.keyCode = 32;//keyCode=32 空格
            $('#tags').trigger(e);


            var tagsValue = $valuesTags.val().replace(/^,|,$/g, '').split(',');
            if (tagsValue.length < 3 && tagsValue.length > 0) { //tags num >1 and <3
                $("<ul><li>请至少输入3个兴趣标签，这样会让别人更加了解你哦！</li></ul>").appendTo(".interest-tags .help-block");
                $(".control-group.interest-tags").addClass("error");
                return false;
            }


            if (!$("input,select,textarea").not("[type=submit]").jqBootstrapValidation("hasErrors")) {
                $("#tags").remove();
                $valuesTags.attr('name', 'tags');
            }
            return true;
        });

        function hasTag(tag) {
            tag = tag.replace(/\s+/g, '')
            return ("," + $tagsValues.val().replace(/\s+/g, '') + ",").indexOf(',' + tag + ',') >= 0;
        }

        function addTagValue(tag) {
            tag = tag.replace(/\s+/g, '')
            $tagsValues.val(($tagsValues.val() + ',' + tag + ',').replace(/,+/g, ','))
        }

        function removeTagValue(tag) {
            tag = tag.replace(/\s+/g, '')
            $tagsValues.val(("," + $tagsValues.val().replace(/\s+/g, '') + ",").replace(',' + tag + ',', ',').replace(/,+/g, ','))
        }

        $(".hot-tags li").live('click', function () {
            var $input = $("#tags");
            var tagValue = $(this).text().replace('+ ', '');

            if (!hasTag(tagValue)) {
                addTagValue(tagValue)
                var $item = $('<li class="as-selection-item"></li>').click(function () {
                    $(this).addClass("selected");
                });
                var $close = $('<a class="as-close">&times;</a>').click(function () {
                    removeTagValue(tagValue)
                    $(this).parent('li').remove();
                    selectionRemoved($item);
                    $input.click();
                    return false;
                });
                $("#as-original-tags").before($item.html(tagValue).prepend($close));
                $input.focus();
            }
            $(this).addClass("selected");
        });

        $("#change_hot_tags").click(function () {
//            $(".hot-tags").show();
                var page = $(this).attr('page');
                var url = $(this).attr('href') + "?page=" + page;
                var $hotTagsWrapper = $("ul.hot-tags");
                $(this).attr('page', parseInt(page) + 1);
                //fetch from cache
                var $tagsForPage = $hotTagsWrapper.find("li.p" + page);
                if ($tagsForPage.length) {
                    $hotTagsWrapper.find("li:visible").hide();
                    $tagsForPage.show();
                } else {
                    $.get(url, function (tags) {
                        if (tags.length == 0) {
                            $("#change_hot_tags").attr('page', 1).click()
                        } else {
                            $hotTagsWrapper.find("li:visible").hide()
                            for (var i = 0; i < tags.length; i++) {
                                var $newTag = $("<li class='as-selection-item p" + page + "'><em class='add-icon'>+ </em>" + tags[i].value + "</li>");
                                if (hasTag(tags[i].value)) {
                                    $newTag.addClass("selected");
                                }
                                $hotTagsWrapper.append($newTag)
                            }
                        }
                    });
                }
                return false;
            }
        ).click();
        function setChatAvatar(avatar){
            if(typeof chatApp != "undefined" && chatApp.myProfile){
                chatApp.myProfile.set("avatarUrl", avatar)
            }
        }
        //upload avatar
        $("#id_avatar_for_upload").change(function () {
            $("#avatar_alert").remove();
            var options = {
//                target: '#crop_avatar_wrapper', // target element(s) to be updated with server response
                beforeSubmit: function () {
                    $("#alert-avatar-upload").html("")
                    $(".avatar .loading").show();
                }, // pre-submit callback
                success: function (data) {
                    var data, big_avatar_url, small_avatar_url, avatar_error
                    try{
                        data = $.parseJSON(data)
                        big_avatar_url = data.big_avatar_url
                        small_avatar_url = data.small_avatar_url
                        avatar_error = data.avatar
                        if (avatar_error) {
                            $("#alert-avatar-upload").html(avatar_error[0])
                            return false;
                        }
                    } catch(e){
                         $("#alert-avatar-upload").html("请您上传不超4MB的头像")
                        return false;
                    } finally{
                        $(".avatar .loading").hide();
                    }
                     $("#avatar-wrapper").find("img").attr('src', big_avatar_url)
                    setChatAvatar(small_avatar_url)
                    $('#crop-avatar-link').show().click();
                    return false;
                },  // post-submit callback
                error: function(){
                    $(".avatar .loading").hide();
                      $("#alert-avatar-upload").html("请您上传不超4MB的头像")
                }
            };
            $("#upload_avatar_form").ajaxSubmit(options);

        });

        $("#crop-avatar-link").click(function () {

            $("#crop_avatar_wrapper").load($('#crop-avatar-link').attr('href'), function () {
                $("#crop_submit").click(function () {

                $("#id_crop_form").ajaxSubmit({
                    success: function (data) {
                        //noinspection JSUnresolvedVariable
                        $("#avatar-wrapper").find("img").attr('src', $.parseJSON(data).big_avatar_url);
                        setChatAvatar($.parseJSON(data).small_avatar_url)
                        $("#crop_avatar_modal").modal('hide');
                        return false;
                    }
                });
                return false;
            })
                $("#crop_avatar_modal").modal();
            });
            return false;
        });


        //crop avatar

    }
    if ($("#create-meal-page")[0]) {

        var $minPersons = $("#id_min_persons");

        $("#id_topic, #id_introduction").jqBootstrapValidation();
        $("#create_meal_form").submit(function () {
            if (!$("#id_menu_id").val()) {
                $("#choose-restaurant-msg").html('<ul class="errorlist"><li>请您在左边选择一个套餐</li></ul>');
                return false;
            }
            return true;
        });
        function getMenuList(numPersons, menuIdToSelect) {
            $("#choose-menu-wrapper").css('visibility', 'hidden');
            var $ajax_loader = $('#loading-menus');
            $ajax_loader.show(1, function () {
                $.get($("#data").data('menu-list-link'), {num_persons: numPersons}, function (data) {
                    $ajax_loader.hide();
                    $("#choose-menu-wrapper").html(data).css('visibility', 'visible');
                    $("#choose-restaurant-msg").clone(true).appendTo("#choose-restaurant-info").show();
                    $("#id_menu_id").val("");
                    if (menuIdToSelect) {
                        $("li[menu-id=" + menuIdToSelect + "]").click();
                    }

                    var $restaurantList = $("#restaurant-list");
                    if ($restaurantList.find("ul li").length >= 5) {
                        $restaurantList.find("ul li:last").css('border-bottom-width', '0');
                        if(!$.browser.msie  || parseInt($.browser.version,10)>8){
                            $restaurantList.lionbars();
                        }

                        $("#lb-wrap-0-restaurant-list").css('height', 377)
                    }


                }, 'html');
            })
        }

//        $("#id_privacy").dropkick({width: 313, startSpeed: 0});

        var $startDateInput = $("#id_start_date");
        $startDateInput.css('visibility', 'visible').datepicker({
            format: 'yyyy-mm-dd',
            todayHighlight: true,
            startDate: $startDateInput.data('startDate'),
            endDate: $startDateInput.data('endDate')
        });


        $('#id_start_time').dropkick({width: 116, startSpeed: 0});
        $minPersons.dropkick({
                width: 313,
                startSpeed: 0,
                change: function (value) {
                    getMenuList(value);
                }
            }
        );
        $('#id_list_price,#id_region').dropkick({width: 120, startSpeed: 100});
        var oldMenuId = $("#id_menu_id").val();
        getMenuList($minPersons.find("option:selected").val(), oldMenuId);

        $("li.restaurant-item").live("click", function () {
            $("#menu-info-wrapper").show();
            $("#choose-restaurant-info").hide();
            var oldMenuId = $(this).siblings(".selected").attr("menu-id");
            $("#menu-" + oldMenuId).hide();
            $(this).addClass('selected').siblings().removeClass("selected");
            $("#menu-" + $(this).attr("menu-id")).show();
            $("#id_menu_id").val($(this).attr("menu-id"));
        });
        $(".map-link").live("click", function () {
            var $mapLink = $(this);
            $("#show_map_modal").modal().on('shown', function () {
                $('#map').gmap3({
                    marker: {
                        latLng: [$mapLink.attr('lat'), $mapLink.attr("long")]
                    },
                    map: {
                        options: {
                            zoom: 15
                        }
                    }
                });
//                $("#map").gmap3({trigger:"resize"})
            });
            return false;
        })
    }

    var $userContainer = $('#user-container');
    var $profile_basic_info_page = $("#profile_basic_info_page");
    var $tagItems = $(".tags li:not(.showing-tag)")
    if (($userContainer[0] || $profile_basic_info_page[0])) {
        $tagItems.live("mouseenter",function () {
            $(this).attr("title", '点击查看该标签下的用户');
        }).live('click', function () {
                window.location.href= $data.data('userListUrl')+"?tags=" + $(this).text()
            })
    }

    if ($userContainer[0]) {
        $(".add-tag-link").click(function () {
            var tag = $(this).data('tags')
            $.post($data.data("add-tag-url"), {'tag': tag}, function () {
                noty({text: tag + " 已经添加到我的兴趣", timeout: 500});
                $(".add-tag-link").remove()
                $(".tags li:contains(" + tag + ")").not('.showing-tag').each(function () {
                    if ($(this).text().trim() == tag) {
                        $(this).addClass("common")
                    }
                })
            });
            return false
        })
        $tagItems.each(function () {
            //noinspection JSUnresolvedVariable
            if ($.inArray($(this).text().trim(), myTags) > -1) {
                $(this).addClass('common');
            }
        });
        $userContainer.imagesLoaded(function () {
            $userContainer.masonry({
                itemSelector: '.box'
//                isAnimated: !Modernizr.csstransitions
            }, function () {
                if ($(document).height() <= $(window).height()) {
                    $(window).scroll();
                }
                $("#need_edit_tags_again_tip").show();
            });
        });
        $(window).resize(function(){
            var orginalWindowWidth = $data.data("windowWidth"), currentWindowWidth = $(window).width()
            if (orginalWindowWidth && orginalWindowWidth != currentWindowWidth) {
                $data.data("windowWidth", currentWindowWidth)
                if ($userContainer.data("masonry")) {
                    $userContainer.masonry('destroy').masonry({
                        itemSelector: '.box'
//                        isAnimated: !Modernizr.csstransitions
                    })
                }
            } else if(! orginalWindowWidth){
                $data.data("windowWidth", currentWindowWidth)
            }
        })

        var ajaxLoaderImageId = $data.data("ajax-load-image-id");
        $userContainer.infinitescroll({
                navSelector: '#page-nav', // selector for the paged navigation
                nextSelector: '#page-nav a', // selector for the NEXT link (to page 2)
                itemSelector: '.box', // selector for all items you'll retrieve
                animate: false,
//                debug:true,
//                path: $data.data("next-page-url"),
                maxPage: $data.data("maxPage"),
                errorCallback: function (a, b, c) {

                    var $need_edit_tags_again_tip = $("#need_edit_tags_again_tip");
                    if ($need_edit_tags_again_tip[0]) {
                        $need_edit_tags_again_tip.show();
                        var scrollTo = $(window).scrollTop() + $need_edit_tags_again_tip.height() + 100 + 'px';
                        $('html,body').animate({ scrollTop: scrollTo }, 800);
                    }
                },
                extendFinished: function (responseText) {
                    var $alert = $(responseText).siblings("div.alert")
                    if ($alert[0]) {
                        $("#main-container").append($alert);
                    }
                },
                loading: {
                    msgText: '加载中...',
                    finishedMsg: '没有了！',
                    img: ajaxLoaderImageId
                }
            },
            // trigger Masonry as a callback
            function (newElements) {
                // hide new items while they are loading
                var $newElems = $(newElements).css({ opacity: 0 });
                // ensure that images load before adding to masonry layout
                $newElems.imagesLoaded(function () {
                    $newElems.animate({ opacity: 1 });
//                    $(newElements).find("img.lazy").lazyload({ threshold: 400, effect: 'fadeIn' });
                    $userContainer.masonry('appended', $newElems, true, function () {
                        if ($(document).height() <= $(window).height()) {
                            $(window).scroll();
                        }
                    });
                });
                $(newElements).find(".tags li").each(function () {
                    //noinspection JSUnresolvedVariable
                    if ($.inArray($(this).html(), myTags) > -1) {
                        $(this).addClass('common');
                    }
                });
            }
        );
    }

    var notyMsg = $data.data("notyMsg");
    if (notyMsg) {
        noty({text: notyMsg})
    }
})

function showPreview(coords) {
    var rxBig = 180 / coords.w;
    var ryBig = 180 / coords.h;
    var rxMiddle = 80 / coords.w;
    var ryMiddle = 80 / coords.h;
    var $avatarInput = jQuery("#id_avatar");
    var originalWidth = $avatarInput.data('org-width');
    var originalHeight = $avatarInput.data('org-height');
    jQuery('#preview_big').css({
        width: Math.round(rxBig * originalWidth) + 'px',
        height: Math.round(ryBig * originalHeight) + 'px',
        marginLeft: '-' + Math.round(rxBig * coords.x) + 'px',
        marginTop: '-' + Math.round(ryBig * coords.y) + 'px'
    });
    jQuery('#preview_middle').css({
        width: Math.round(rxMiddle * originalWidth) + 'px',
        height: Math.round(ryMiddle * originalHeight) + 'px',
        marginLeft: '-' + Math.round(rxMiddle * coords.x) + 'px',
        marginTop: '-' + Math.round(ryMiddle * coords.y) + 'px'
    });
}
