$(document).ready(function () {

    $("#restaurant-nav li").removeClass("active");
    $("#" + $("#nav-active-id").html()).addClass("active")

    //dish list page
    if ($("#dish-list")[0]) {

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
        $('#checkin-form')[0] && $('#checkin-form').ajaxForm({target:'#result', beforeSubmit:function () {
            var code = $("#id_code").val();
            if (!code || code.length != 8) {
                alert('请输入8位验证码！')
                return false;
            }
        } });

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
    }

//    for add menu page
    if ($("#dish-container")[0]) {

        $("#add-menu-help-link").click(function () {
            $("#add-menu-help-dialog").dialog({
                autoOpen:true,
                title:"操作帮助",
                modal:true,
                width:550,
                position:['center', 100]
            });
            return false;
        })

        //drag category
        $("#dish-container dt, #dish-container dd").draggable({
            connectToSortable:"#menu-items",
            revert:"invalid",
            helper:helperMasker,
            cursor:"move",
            opacity:0.35
        });

        $("#menu-items").sortable({
            cursor:"move",
            placeholder:"ui-state-highlight",
            forcePlaceholderSize:true,
            containment:"#menu-items",
            receive:function (e, ui) {
                hideDishes(ui.sender.attr("dish-id"));
            }
        });


        $("#dish-container dd,#dish-container dt").live('dblclick', function (e) {
            $(this).clone().appendTo($("#menu-items")).hide().fadeIn(1000);
            hideDishes($(this).attr("dish-id"))
        })

        $("#menu-items dt").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
        })
        $("#menu-items dt .close").live('click', function (e) {
            $(this).parents("dt").fadeOut(1000).remove();
            return false;
        })
        $("#menu-items dd").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
            showDishes($(this).attr("dish-id"))
        });
        $("#menu-items dd .close").live('click', function (e) {
            $(this).parents("dd").fadeOut(1000).remove();
            showDishes($($(this).parents("dd")).attr("dish-id"))
        })

        $("#menu-container,#dish-container").disableSelection();


        $("#add-category-link").click(function () {
            $("#add-category-dialog").dialog({
                autoOpen:true,
                modal:true,
                width:250,
                resizable:false,
                position:['center', 100],
                buttons:{
                    确定:function () {
                        var $category = $("#category-name");
                        if (!$category.val()) {
                            $category.focus();
                        } else {
                            //submit request
                            $("#add-dish-category").ajaxSubmit(function (data) {
                                //create category
                                var $category_dt;
                                if (Boolean(data.created)) {
                                    $category_dt = $('<dt class="category tag ui-draggable" category-id="' + data.id + '">' + data.name + '<a href="#" class="close cb">×</a></dt>')
                                    $category_dt.hide().appendTo($("#dish-list")).draggable({
                                        connectToSortable:"#menu-items",
                                        revert:"invalid",
                                        helper:helperMasker,
                                        cursor:"move",
                                        opacity:0.35
                                    }).show();
                                } else {
                                    $category_dt = $("#dish-list [category-id=" + data.id + "]")
                                }
                                $category_dt.dblclick();
                                $category.val("");
                                $("#add-category-dialog").dialog("close");
                            })
                        }
                    },
                    取消:function () {
                        $(this).dialog("close");
                    }
                }
            });
            return false;
        })

        $("#save-menu-form").submit(function () {

            if ($("#menu-items").children().length == 0) {
                alert("请拖拽左边的分类或者菜到邮编的套餐栏中")
                return false;
            }
            $("#save-menu-btn").addClass("disabled")
            var postData = {};
            var $menuItems = $("#menu-items").children();
            var items = $menuItems.map(function (i, elem) {
                $item = $(elem);
                if ($item.is(".dish")) {
                    return  { id:$item.attr('dish-id'), num:$item.find(" .num").text() };
                } else {
                    return  { id:$item.attr('category-id') };
                }

            }).get();
            postData = {num_persons:$("#id_num_persons").val(), average_price:$("#id_average_price").val(), items:items}

            $.post($(this).attr("href"), JSON.stringify(postData), function (data) {
                window.location.href = data.url
            }, "json")
            return false;
        })


    }
//end of add menu page

//for menu list page
    if ($("#menu-list")[0]) {
        var $container = $('#menu-list');

        $container.masonry({
            itemSelector:'.menu-container',
            columnWidth:375,
            gutterWidth:30

        });
        $(".dellink").click(function (e) {
            var delUrl = $(this).attr('href');
            $("<div>确定要删除套餐吗？</div>").dialog({
                autoOpen:true,
                dialogClass:"confirm",
                modal:true,
                width:200,
                height:110,
                resizable:false,
                position:'center',
                buttons:{
                    确定:function () {
                        $.post(delUrl, function (data) {
                            window.location.href = data.url
                        }, 'json')
                    },
                    取消:function () {
                        $(this).dialog("close");
                    }
                }
            });
            return false;
        })

    }

})
;

function helperMasker() {
    return $(this).clone().addClass("helper").css("width", $(this).width())
}

function hideDishes(dishId) {
    $("#dish-container [dish-id=" + dishId + "]").hide();
}

function showDishes(dishId) {
    $("#dish-container [dish-id=" + dishId + "]").fadeIn(1000);
}