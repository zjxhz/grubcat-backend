jQuery(function ($) {

    $("#restaurant-nav li").removeClass("active");
    $("#" + $("#data").data("nav-active-id")).addClass("active");
    // bind form using 'ajaxForm'
    $('#checkin-form')[0] && $('#checkin-form').ajaxForm({target:'#result', beforeSubmit:function () {
        var code = $("#id_code").val();
        if (!code || code.length != 8) {
            alert('请输入8位验证码！')
            return false;
        }
        $("#result").html("");
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

        $("#save-menu-btn").click(function () {
            $("#save-menu-form").submit();
        })
        $("#save-menu-form").submit(function () {

            if (!$("#id_num_persons").val()) {
                alert("请输入就餐人数")
                return false;
            }

            if (!$("#id_average_price").val()) {
                alert("请输入均价")
                return false;
            }

            if (!$("#id_name").val()) {
                alert("请输入套餐名")
                return false;
            }

            if ($("#menu-items").children().length == 0) {
                alert("请拖拽左边的分类或者菜到邮编的套餐栏中")
                return false;
            }
            $("#save-menu-btn").addClass("disabled").attr("disabled", true)
            var postData = {};
            var $menuItems = $("#menu-items").children();
            var items = $menuItems.map(function (i, elem) {
                var $item = $(elem);
                if ($item.is(".dish")) {
                    return  { id:$item.attr('dish-id'), num:$item.find(" .num").text() };
                } else {
                    return  { id:$item.attr('category-id') };
                }

            }).get();
            postData = {num_persons:$("#id_num_persons").val(), average_price:$("#id_average_price").val(), name:$("#id_name").val(), items:items}

            $.post($(this).attr("href"), JSON.stringify(postData), function (data) {
                if (data.status == 'OK') {
                    window.location.href = data.url
                } else {
                    alert(data.message)
                    $("#save-menu-btn").removeClass("disabled").removeAttr("disabled")
                }

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
            columns:2,
//            columnWidth:360
            gutterWidth:30

        });
        $(".menu-cover-wrapper.has-cover").hover(function () {
            $(this).find(".upload-actions, .upload-actions-bg").show();
        }, function () {
            $(this).find(".upload-actions, .upload-actions-bg").hide();
        })
        $(".btn-crop-cover").click(function () {
            var $menuContainer = $(this).parents(".menu-container");
            $("#crop_menu_cover_wrapper").load($menuContainer.data("crop-cover-url"), function () {
                $("#crop_cover_modal").modal();
                $("#crop_submit").click(function () {
                    $("#id_crop_form").ajaxSubmit({
                        success:function (data) {
                            //noinspection JSUnresolvedVariable
                            $menuContainer.find(".menu-cover-wrapper img").attr("src", data.normal_cover_url);
                            $("#crop_cover_modal").modal('hide')
                        }
                    })
                })
            })
        })

        //upload menu cover
        $(".upload-cover-input").change(function () {
            var $menuCoverWrapper = $(this).parents(".menu-cover-wrapper");
            var options = {
//                target:'#crop_menu_cover_wrapper', // target element(s) to be updated with server response
                beforeSubmit:function () {
                    $(".loading").show();
                }, // pre-submit callback
                success:function (data) {
                    $(".loading").hide();
                    //noinspection JSUnresolvedVariable
                    $menuCoverWrapper.find("img").attr('src', data.normal_cover_url);
                    $menuCoverWrapper.addClass("has-cover");
                    $menuCoverWrapper.find(".btn-upload-cover").removeClass("btn-danger").addClass("btn-primary");
                    $menuCoverWrapper.find(".upload-actions, .upload-actions-bg").show();
                    $menuCoverWrapper.hover(function () {
                        $(this).find(".upload-actions, .upload-actions-bg").show();
                    }, function () {
                        $(this).find(".upload-actions, .upload-actions-bg").hide();
                    })
                    $menuCoverWrapper.find(".btn-crop-cover").click();
                    return false;
                }
            };
            $menuCoverWrapper.find("form.upload_menu_cover_form").ajaxSubmit(options);

        });

        $(".dellink").click(function (e) {
            var $menuContainer = $(this).parents(".menu-container");
            var delUrl = $(this).attr('href');
            var $delMenuModal = $("#del-menu-modal");
            $("#btn-del").unbind("click").click(function () {
                $.post(delUrl, function () {
                    $delMenuModal.modal("hide");
                    $menuContainer.fadeOut(1000).remove();
                    noty({text:"套餐删除成功"});
                    if ($(".menu-container").length) {
                        $container.masonry('reload');
                    } else {
                        window.location.reload();
                    }
                })
            })
            $delMenuModal.modal();
            return false;
        })

    }


    //for today meal list
    if ($("#today-meal-list")[0]) {
        $(".menu-detail-link").click(function () {

            $("#menu-detail-modal-wrapper").load($(this).attr("href"), function (html) {
                $("#menu-detail-modal").modal()
            });
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

function showPreview() {

}