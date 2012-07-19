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

//    for menu page
    if ($("#dish-container")[0]) {
        $(".help-title a.help-link").click(function () {
            $(".help-content").slideToggle(1000);
            $("a.hide-link").toggleClass('hide')
            return false;
        })

        $(".help-title a.hide-link").click(function () {
            $(".help-content").slideUp(1000);
            $(this).hide();
            return false;
        })

        //drag category
        $("#dish-container dt, #dish-container dd").draggable({
            connectToSortable:"#menu-container",
            revert:"invalid",
            helper:helperMasker,
            cursor:"move",
            opacity:0.35
        });

        $("#menu-container").sortable({
            cursor:"move",
            placeholder:"ui-state-highlight",
            forcePlaceholderSize:true,
            containment:"#menu-container",
            receive:function (e, ui) {
                hideDishes(ui.sender.attr("dish-id"));
            }
        });


        $("#dish-container dd,#dish-container dt").live('dblclick', function (e) {
            $(this).clone().appendTo($("#menu-container")).hide().fadeIn(1000);
            hideDishes($(this).attr("dish-id"))
        })

        $("#menu-container dt").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
        })
        $("#menu-container dt .close").live('click', function (e) {
            $(this).parents("dt").fadeOut(1000).remove();
            return false;
        })
        $("#menu-container dd").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
            showDishes($(this).attr("dish-id"))
        });
        $("#menu-container dd .close").live('click', function (e) {
            $(this).parents("dd").fadeOut(1000).remove();
            showDishes($($(this).parents("dd")).attr("dish-id"))
        })

        $("body").disableSelection();

        $("#add-category").submit(function () {
            return false;
        })

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
                                        connectToSortable:"#menu-container",
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

        $("#save-menu").click(function () {
            var postData = {};
//            TODO chagne to #menu-container
            var $menuItems = $("#dish-list").children();
            var items = $menuItems.map(function( i, elem ){
                $item = $(elem);
                if($item.is(".dish"))
                {
//                , num:$item.find(">.num").text()
                    return  {type:"dish", id:  $item.attr('dish-id') };
                } else
                {
                    return  {type:"category", id:  $item.attr('category-id') };
                }

            }).get();
            postData = {num_persons:8,average_price:30,items:items}

            $.post($(this).attr("href"), JSON.stringify(postData), function(data){
                alert(data.message)
            }, "json")
            return false;
        })
    }

});

function helperMasker() {
    return $(this).clone().addClass("helper").css("width", $(this).width())
}

function hideDishes(dishId) {
    $("#dish-container [dish-id=" + dishId + "]").hide();
}

function showDishes(dishId) {
    $("#dish-container [dish-id=" + dishId + "]").fadeIn(1000);
}