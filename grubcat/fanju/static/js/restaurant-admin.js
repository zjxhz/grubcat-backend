jQuery(function ($) {
    var $data = $("#data")

    $("#restaurant-nav li").removeClass("active");
    $("#" + $("#data").data("nav-active-id")).addClass("active");


    /************************** 客人就餐 ****************************/
    // bind form using 'ajaxForm'
    $('#checkin-form')[0] && $('#checkin-form').ajaxForm({target:'#result', beforeSubmit:function () {
        var code = $("#id_code").val();
        if (!code || code.length != 8) {
            alert('请输入8位验证码！')
            return false;
        }
        $("#result").html("");
    } });



    /************************** dish list pag ****************************/
    var $dishListPage = $("#dish-list-page")
    if ($dishListPage[0]) {
        var $addOrEditDishModal = $("#add-edit-dish-modal"),
            $addOrEditDishModalBody = $addOrEditDishModal.find(".modal-body"),
            $addDishLink = $("#add-dish-link")

        $("body").keyup(function (e) {
            if (e.which == 78 || e.which == 110) {
                $addDishLink.click()
            }
        })
        $addOrEditDishModal.keyup(function (e) {
            if (e.which == 13) {
                $("#btn-add-edit-dish").click()
            }
            if (e.which == 78 || e.which == 110) {
                return false
            }
        })

        $addDishLink.click(function(){
            $addOrEditDishModal.data('dish-action','add')
        })
        $(".changelink").live('click',function(){
            $addOrEditDishModal.data('dish-action','edit')
        })

        $("#add-dish-link,.changelink").live('click', function () {
            $.get($(this).attr('href'), function (html) {
                $addOrEditDishModalBody.html(html)
                if ($addOrEditDishModal.data('dish-action') == 'add') {
                    $("#id_categories").val($addOrEditDishModal.data('last-dish-categories')).find("option:selected").prependTo($("#id_categories"))
                }
                $addOrEditDishModal.modal({show:true,backdrop:'static'})
            })
            return false
        })

        //make sure each time edit using a different dialog model
        $addOrEditDishModal.on('hidden',function(){

            $addOrEditDishModal.removeData("modal")
            $addOrEditDishModalBody.empty()
        }).on('shown',function(){
                $("#id_name").focus()
            })



        $("#add-category-link").live('click', function () {

            bootbox.prompt({
                text:'添加分类',
                confirm: function(categoryName) {
                    if (!categoryName) {
                        return false
                    } else {
                        //submit request
                        $.post($data.data("add-dish-category-link"), {'category-name': categoryName}, function (data) {
                            //create category
                            var $catgegoryOption
                            if (Boolean(data.created)) {
                                $catgegoryOption = $("<option value='" + data.id +"'>" + data.name + "</option>")
                                $catgegoryOption.prependTo("#id_categories")
                            }

                        })
                    }
                }
            });

            return false
        })

        //add or edit a dish
        $("#btn-add-edit-dish").click(function(){
            $("#form-add-edit-dish").ajaxSubmit({
                success:function(html){
                    var $res = $(html)
                    if($res.is("tr")){
                        //success
                        if($addOrEditDishModal.data('dish-action')=='add'){
                            $addOrEditDishModal.data('last-dish-categories', $("#id_categories").val())
                        }
                        $addOrEditDishModal.modal('hide')

                        var id = $res.attr("id")
                        if($dishListPage.find("#"+id)[0]){
                            //update a dish
                            $res.hide().replaceAll($dishListPage.find("#" + id)).fadeIn()
                        } else {
                            //a new dish
                            $res.hide().prependTo($dishListPage.find("tbody")).fadeIn()
                        }
                    } else {
                        $addOrEditDishModalBody.html($res)
                    }
                }
            })
        })


        $("a.dellink").live('click', function(){
            var $link = $(this);

            bootbox.confirm({
                text: "确定要删除 “" + $link.parents("tr").find("td:first").text() + "” 这道菜吗？",
                confirmClass: 'btn-danger',
                confirmLabel: '删除',
                confirm: function () {
                    $.post($link.attr('href'), function () {
                        $link.parents("tr").fadeOut(300, function(){
                            $(this).remove()
                        });

                    })
                }})
            return false;
        })
    }

    /**************************  add or edit menu page ****************************/
    if ($("#add-edit-menu-page")[0]) {
        var $menuItems = $("#menu-items"), $dishList = $("#dish-list")


        function helperMasker() {
            return $(this).clone().addClass("helper").css("width", $(this).width())
        }

        function hideDishes(dishId) {
            $dishList.find(".dish[dish-id=" + dishId + "]").hide();
        }

        function showDishes(dishId) {
            $dishList.find(".dish[dish-id=" + dishId + "]").fadeIn(1000);
        }


        function calculatePrice() {
            calculateTotalPrice()
            calculateAveragePrice()
        }

        function calculateTotalPrice() {
            var $totalPrice = $("#total-price"), $menuContainer = $("#menu-items"), totalPrice = parseFloat($totalPrice.text())
            totalPrice = 0
            $menuContainer.find(".dish").each(function () {
                totalPrice += parseFloat($(this).data('price')) * parseFloat($(this).find('.num').text())
            })
            $totalPrice.text(totalPrice).fadeOut(50).fadeIn(1000)
        }

        function calculateAveragePrice() {
            var totalPrice = parseFloat($("#total-price").text())
            //calculate average price
            var $numPersons = $("#id_num_persons"), numPersons = parseInt($numPersons.val())
            if (numPersons > 0) {
                $("#id_average_price").val((Math.floor(totalPrice * 10 / numPersons) / 10).toFixed(1))
            }
        }

        function calculateDishNumPerCategory(){
            $menuItems.find(".category").each(function(){
                var $category = $(this)
                $category.find(".dish-num-per-category").text("(" + $category.nextUntil(".category").length + ")")
            })
        }
        calculateDishNumPerCategory()
        $("#add-category-link").click(function () {

            bootbox.prompt({
                text:'添加分类',
                confirm: function(categoryName) {
                    if (!categoryName) {
                        return false
                    } else {
                        //submit request
                        $.post($data.data("add-dish-category-link"), {'category-name': categoryName}, function (data) {
                            //create category
                            var $category_dt;
                            if (Boolean(data.created)) {
                                $category_dt = $('<dt class="category ui-draggable" category-id="' + data.id + '">' + data.name + '<span class="dish-num-per-category"></span><a href="#" class="close cb">×</a></dt>')
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
                        })
                    }
                }
            });

            return false
        })

        //remove existing dishes in left column if edit a menu
        $menuItems.find(".dish").each(function(){
            $dishList.find(".dish[dish-id=" + $(this).attr('dish-id') + "]").hide()
        })

        $("#add-menu-help-link").click(function () {

            $("#add-menu-help-modal").modal('show')
            return false;
        })

        //drag category
        $dishList.find(".dish, .category").draggable({
            connectToSortable:"#menu-items",
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
                calculateDishNumPerCategory()
                hideDishes(ui.sender.attr("dish-id"));
                $(this).find(".num").tooltip({title:'修改',selector:true, delay:{show:300}})
            },
            update:function(){
                calculateDishNumPerCategory()
            }
        });


        //add dish and category
        $("#dish-list .category, #dish-list .dish").live('dblclick', function (e) {
            $(this).clone().appendTo($menuItems).hide().fadeIn(1000).find(".num").tooltip({title:'修改',selector:true, delay:{show:300}});
            hideDishes($(this).attr("dish-id"))
            calculatePrice()
            calculateDishNumPerCategory()
        })

        //remove category
        $menuItems.find(".category").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
            calculateDishNumPerCategory()
            e.preventDefault()
        })
        //remove category
        $menuItems.find(".category .close").live('click', function (e) {
            $(this).parents(".category").fadeOut(1000).remove();
            calculateDishNumPerCategory()
            e.preventDefault()
        })
        //remove dish
        $menuItems.find(".dish").live('dblclick', function (e) {
            $(this).fadeOut(1000).remove();
            calculatePrice()
            calculateDishNumPerCategory()
            showDishes($(this).attr("dish-id"))
             e.preventDefault()
        });
        //remove dish
        $menuItems.find(".dish .close").live('click', function (e) {
            $(this).parents(".dish").fadeOut(1000).remove();
            calculatePrice()
            calculateDishNumPerCategory()
            showDishes($($(this).parents(".dish")).attr("dish-id"))
            e.preventDefault()
        })


        $menuItems.find(".dish .num").live('click',function () {
            var $dishNum = $(this)
            bootbox.prompt({
                text:'更改份数',
                defaultValue: $dishNum.text(),
                confirm: function (num) {
                    try {
                        num = parseInt(num)
                        //todo reg check
                    } catch (e) {
                        return false
                    }

                    if (!num) {
                        return false
                    } else {
                        $dishNum.text(num)
                        calculatePrice()
                    }
                }

            })
            return false;
        }).tooltip({title:'修改',selector:true, delay:{show:300}})


        $("#menu-items,#dish-list").disableSelection();

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
    if ($("#menu-list-page")[0]) {
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
                    if(!$(".menu-cover-wrapper:not(.has-cover)")[0]){
                        $("#no-cover-tip").remove()
                    }
                    return false;
                }
            };
            $menuCoverWrapper.find("form.upload_menu_cover_form").ajaxSubmit(options);

        });

        $(".dellink").click(function (e) {
            var $menuContainer = $(this).parents(".menu-container");
            var delUrl = $(this).attr('href');
            bootbox.confirm({
                text:'确定要删除该套餐吗？',
                confirmClass: 'btn-danger',
                confirmLabel: '删除',
                confirm: function () {
                    $.post(delUrl, function () {
                        $menuContainer.fadeOut(1000).remove();
                        noty({text: "套餐删除成功"});
                        if ($(".menu-container").length) {
                            $container.masonry('reload');
                        } else {
                            window.location.reload();
                        }
                    })
                }
            })

            return false;
        })

    }


    //for today meal list
    if ($("#today-meal-list-page")[0]) {
        $(".menu-detail-link").click(function () {

            $("#menu-detail-modal-wrapper").load($(this).attr("href"), function (html) {
                $("#menu-detail-modal").modal()
            });
            return false;
        })
    }

});

function showPreview() {

}