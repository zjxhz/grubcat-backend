(function ($) {
    if ($("#faq")[0]) {

        $("#faq .sidebar-box-content a").click(function () {
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
        $("img.lazy").lazyload({ threshold:200, effect:'fadeIn' });
    }

    if ($("#meal-detail")[0]) {
//    $("select").dropkick({width:30, startSpeed:0})
        $("#id_num_persons").change(function () {
            $("#total_price").html($("#meal_price").html() * $(this).val());
        })
        $(".btn-book-now").click(function () {
            $("#order_info_form").submit();
            return false;
        })

    }

    if ($("#edit-profile")[0] || $("#bind-edit-profile")[0]) {
        $("#profile-nav-info").addClass("active");
        var user_tags = $("#id_tags").val();
        $("#id_tags").autoSuggest($("#data").attr('list-tags-url'), {
            asHtmlID:'tags',
            preFill:user_tags,
            neverSubmit:true,
            startText:'请输入你的兴趣爱好，这样别人会更好地了解你，系统也会优先展示和你有共同兴趣的朋友'
        })
        $('#tags').parents().find('form').submit(function () {
            $("#tags").remove();
            $("#as-values-tags").attr('name', 'tags');
        });

        $(".interest-tags").click(function(){
            $(".hot-tags").show()
        })

        $(".hot-tags li").live('click', function () {
            var $input = $("#tags");
            var valueToAdd = $(this).text().replace('+ ', '');
            var $tagsValues = $("#as-values-tags")
            if (("," + $tagsValues.val().replace(/\s+/g, '')).indexOf(',' + valueToAdd + ',') < 0) {
                $tagsValues.val($tagsValues.val() + valueToAdd + ',');
                var $item = $('<li class="as-selection-item"></li>').click(function () {
                    $(this).addClass("selected");
                })
                var $close = $('<a class="as-close">&times;</a>').click(function () {
                    $tagsValues.val($tagsValues.val().replace("," + valueToAdd + ",", ","));
                    $input.focus();
                    return false;
                });
                $("#as-original-tags").before($item.html(valueToAdd).prepend($close));
            }
            $(this).remove();
        })

        $("#change_hot_tags").click(function(){
            var url = $(this).attr('href') + "?page=" + $(this).attr('page')
            $(this).attr('page', parseInt($(this).attr('page'))+1)

            $.get(url, function(tags){
                $("ul.hot-tags li").remove()
                var tag;
                for (var i=0; i< tags.length; i++){
                    $("ul.hot-tags").append($("<li class='as-selection-item'><em class='add-icon'>+ </em>" + tags[i].value +"</li>"))
                }
                if (tags.length == 0){
                    $("#change_hot_tags").attr('page',1).click()
                }
            })

            return false;
        }).click()

        //upload avatar
        $("#id_avatar_for_upload").change(function () {
            var options = {
                target:'#crop_avatar_wrapper', // target element(s) to be updated with server response
                beforeSubmit:function () {
                    $(".avatar .loading").show();
                }, // pre-submit callback
                success:function (html) {
                    $(".avatar .loading").hide()
                    $("#avatar-wrapper img").attr('src', $("#data-avatar-page").attr('data-big-avatar-url'))
                    $('#crop-avatar-link').show();
                    submit_crop_form();
                    $("#crop_avatar_modal").modal();
                    return false;
                }  // post-submit callback
            };
            $("#upload_avatar_form").ajaxSubmit(options);

        })
        $("#upload-avatar-link").click(function () {
            $("#id_avatar_for_upload").click()
            return false;
        })

        $("#crop-avatar-link").click(function () {

            $("#crop_avatar_wrapper").load($('#crop-avatar-link').attr('href'), function () {
                submit_crop_form();
                $("#crop_avatar_modal").modal();
            })
            return false;
        })

        function submit_crop_form() {
            $("#crop_submit").click(function () {
                $("#id_crop_form").ajaxSubmit({
                    success:function (data) {
                        $("#avatar-wrapper img").attr('src', data.big_avatar_url)

                        $("#crop_avatar_modal").modal('hide');
                        return false;
                    },
                    dataType:'json'        // 'xml', 'script', or 'json' (expected server response type)
                })
                return false;
            })
        }

        //crop avatar

    }
    if ($("#create-meal-page")[0]) {
        function getMenuList(numPersons, menuIdToSelect, if_let_fanjoin_choose) {
            $("#choose-menu-wrapper").css('visibility', 'hidden');
            $ajax_loader = $('#loading-menus');
            $ajax_loader.show(1, function () {
                $.get($("#data").attr('menu-list-link'), {num_persons:numPersons}, function (data) {
                    $ajax_loader.hide();
                    $("#choose-menu-wrapper").html(data).css('visibility', 'visible');
                    $("#choose-restaurant-msg").clone(true).appendTo("#choose-restaurant-info").show();
                    $("#id_menu_id").val("");
                    if (menuIdToSelect) {
                        $("li[menu-id=" + menuIdToSelect + "]").click();
                    }

                    if ($("#restaurant-list ul li").length >= 5) {
                        $("#restaurant-list ul li:last").css('border-bottom-width', '0');
                        $("#restaurant-list").lionbars();
                        $("#lb-wrap-0-restaurant-list").css('height', 377)
                    }


                }, 'html');
            })
        }

        $("#id_privacy").dropkick({width:313, startSpeed:0})

        $.datepicker.regional['zh-CN'] =
        {
            clearText:'清除', clearStatus:'清除已选日期',
            closeText:'关闭', closeStatus:'不改变当前选择',
            prevText:'&lt;上月', prevStatus:'显示上月',
            nextText:'下月&gt;', nextStatus:'显示下月',
            currentText:'今天', currentStatus:'显示本月',
            monthNames:['一月', '二月', '三月', '四月', '五月', '六月',
                '七月', '八月', '九月', '十月', '十一月', '十二月'],
            monthNamesShort:['一', '二', '三', '四', '五', '六',
                '七', '八', '九', '十', '十一', '十二'],
            monthStatus:'选择月份', yearStatus:'选择年份',
            weekHeader:'周', weekStatus:'年内周次',
            dayNames:['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
            dayNamesShort:['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
            dayNamesMin:['日', '一', '二', '三', '四', '五', '六'],
            dayStatus:'设置 DD 为一周起始', dateStatus:'选择 m月 d日, DD',
            dateFormat:'yy-mm-dd', firstDay:1,
            initStatus:'请选择日期', isRTL:false
        };

        $.datepicker.setDefaults($.datepicker.regional['zh-CN']);

        $("#id_start_date").css('visibility', 'visible').datepicker({
            onSelect:function (dateText, inst) {
                $(inst.input).change().focusout();
            },
            defaultDate:"2012-8-17",
            numberOfMonths:1,
            minDate:'+4D',
            maxDate:'+1M'
        })


        $('#id_start_time').dropkick({width:116, startSpeed:0});
        $("#id_min_persons").dropkick({
                change:false,
                width:313,
                startSpeed:0,
                change:function (value, label) {
                    getMenuList(value);
                }
            }
        )
        $('#id_list_price,#id_region').dropkick({width:120, startSpeed:100});
        var if_let_fanjoin_choose = $("#id_if_let_fanjoin_choose").val() == "True";
        var oldMenuId = $("#id_menu_id").val();
        getMenuList($("#id_min_persons>option:selected").val(), oldMenuId, if_let_fanjoin_choose);

        $("li.restaurant-item").live("click", function () {
            $("#menu-info-wrapper").show();
            $("#choose-restaurant-info").hide();
            var oldMenuId = $(this).siblings(".selected").attr("menu-id");
            $("#menu-" + oldMenuId).hide();
            $(this).addClass('selected').siblings().removeClass("selected");
            $("#menu-" + $(this).attr("menu-id")).show();
            $("#id_menu_id").val($(this).attr("menu-id"));
        })
    }
})(jQuery);

function showPreview(coords) {
    var rxBig = 180 / coords.w;
    var ryBig = 180 / coords.h;
    var rxMiddle = 80 / coords.w;
    var ryMiddle = 80 / coords.h;
    var originalWidth = jQuery("#id_avatar").data('org-width');
    var originalHeight = jQuery("#id_avatar").data('org-height');
    jQuery('#preview_big').css({
        width:Math.round(rxBig * originalWidth) + 'px',
        height:Math.round(ryBig * originalHeight) + 'px',
        marginLeft:'-' + Math.round(rxBig * coords.x) + 'px',
        marginTop:'-' + Math.round(ryBig * coords.y) + 'px'
    });
    jQuery('#preview_middle').css({
        width:Math.round(rxMiddle * originalWidth) + 'px',
        height:Math.round(ryMiddle * originalHeight) + 'px',
        marginLeft:'-' + Math.round(rxMiddle * coords.x) + 'px',
        marginTop:'-' + Math.round(ryMiddle * coords.y) + 'px'
    });
}