$(document).ready(function () {
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

    if($("#meal-list")[0]){
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
})
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

    $(document).ready(function () {
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
    })
}