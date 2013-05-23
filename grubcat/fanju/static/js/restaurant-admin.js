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

        var $menuItems = $("#menu-items")
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

        $menuItems.sortable({
            cursor:"move",
            placeholder:"ui-state-highlight",
            forcePlaceholderSize:true,
            containment:"#menu-items",
            receive:function (e, ui) {
                calculatePrice()
                hideDishes(ui.sender.attr("dish-id"));
                $(this).find(".num").tooltip({title:'修改',selector:true, delay:{show:300}})
            }
        });


        $("#dish-container dd,#dish-container dt").live('dblclick', function (e) {
            $(this).clone().appendTo($("#menu-items")).hide().fadeIn(1000).find(".num").tooltip({title:'修改',selector:true, delay:{show:300}});
            hideDishes($(this).attr("dish-id"))
            calculatePrice()
        })

        //remove category
        $menuItems.find("dt").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
        })
        //remove category
        $menuItems.find("dt .close").live('click', function (e) {
            $(this).parents("dt").fadeOut(1000).remove();
            return false;
        })
        //remove dish
        $menuItems.find("dd").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
            calculatePrice()
            showDishes($(this).attr("dish-id"))
        });
        //remove dish
        $menuItems.find("dd .close").live('click', function (e) {
            $(this).parents("dd").fadeOut(1000).remove();
            calculatePrice()
            showDishes($($(this).parents("dd")).attr("dish-id"))
        })

        var $changeDishNumDialog = $("#change-dish-num-dialog")
        function changeDishNum() {
            var $inpuNum = $("#input-change-num");
            var $dishNum = $menuItems.find(".dish[dish-id=" + $changeDishNumDialog.data('dish-id') +"]").find(".num")
            var num = $inpuNum.val()
            if (!num) {
                $inpuNum.focus();
            } else {
                try {
                    $dishNum.text(parseInt(num))
                    //submit request
                    calculatePrice()
                    $changeDishNumDialog.dialog("close");
                } catch (e) {
                    $inpuNum.focus();
                }

            }
        }


        $("#menu-items .dish .num").live('click',function () {
            var $dishNum = $(this)
            $changeDishNumDialog.data('dish-id', $dishNum.parents('.dish').attr('dish-id'))
            $("#input-change-num").val($dishNum.text())
            $changeDishNumDialog.dialog({
                autoOpen:true,
                modal:true,
                width:200,
                resizable:false,
                position:['center', 200],
                buttons:{
                    确定:function(){
                        changeDishNum()
                    },
                    取消:function () {
                        $(this).dialog("close");
                    }
                }
            });
            return false;
        }).tooltip({title:'修改',selector:true, delay:{show:300}})

        $("#input-change-num").keydown(function(e){
            if(e.keyCode==13){
                changeDishNum()
                return false;
            }
        })

        $("#menu-container,#dish-container").disableSelection();

        $("#id_num_persons").change(function () {
            calculateAveragePrice()
        }).keyup(function () {
                calculateAveragePrice()
            }).focus(function () {
                var $tip = $(this).siblings(".help-inline")
                if ($tip.html()) {
                    $tip.html("")
                }
            }).blur(function () {
                var $tip = $(this).siblings(".help-inline")
                if (!$(this).val() && !$tip.html()) {
                    $tip.html("输入后自动计算人均消费")
                }
            })

        $("#add-category-link").click(function () {
            $("#add-category-dialog").dialog({
                autoOpen:true,
                modal:true,
                width:250,
                resizable:false,
                position:['center', 100],
                buttons:{
                    确定:addCategory,
                    取消:function () {
                        $(this).dialog("close");
                    }
                }
            });
            return false;
        })

        function addCategory() {
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
                            connectToSortable: "#menu-items",
                            revert: "invalid",
                            helper: helperMasker,
                            cursor: "move",
                            opacity: 0.35
                        }).show();
                    } else {
                        $category_dt = $("#dish-list [category-id=" + data.id + "]")
                    }
                    $category_dt.dblclick();
                    $category.val("");
                    $("#add-category-dialog").dialog("close");
                })
            }
        }

        $("#category-name").keydown(function(e){
            if (e.keyCode == 13 ) {
                addCategory()
                return false;
            }
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
                alert("请输入人均消费")
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

            var averagePriceInput = parseFloat($("#id_average_price").val())
            var averagePriceCalculated = (Math.floor(parseFloat($("#total-price").text()) * 10 / parseInt($("#id_num_persons").val())) / 10)
            if(averagePriceInput > averagePriceCalculated){
                 alert("您输入的人均消费[" +averagePriceInput + "] 高于系统计算出来的价格[" + averagePriceCalculated +"]，请重新核对下！")
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
        calculateTotalPrice()
        var $tip = $("#id_num_persons").siblings(".help-inline")
        if (!$("#id_num_persons").val() && !$tip.html()) {
            $tip.html("输入后自动计算人均消费")
        } else if($("#id_num_persons").val()){
            $tip.html("")
        }
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
                    $menuCoverWrapper.find(".loading").show();
                }, // pre-submit callback
                success:function (data) {
                    $menuCoverWrapper.find(".loading").hide();
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

 function calculatePrice(){
     calculateTotalPrice()
     calculateAveragePrice()
 }

function calculateTotalPrice() {
    var $totalPrice = $("#total-price"), $menuContainer = $("#menu-container"), totalPrice = parseFloat($totalPrice.text())
    totalPrice = 0
    $menuContainer.find(".dish").each(function () {
        totalPrice += parseFloat($(this).data('price')) * parseFloat($(this).find('.num').text())
    })
    $totalPrice.text(totalPrice).fadeOut(50).fadeIn(1000)
}

 function calculateAveragePrice(){
     var totalPrice = parseFloat($("#total-price").text())
     //calculate average price
     var $numPersons = $("#id_num_persons"), numPersons = parseInt($numPersons.val())
     if(numPersons > 0){
         $("#id_average_price").val((Math.floor(totalPrice*10/numPersons)/10).toFixed(1))
     }
 }

function showPreview() {

}