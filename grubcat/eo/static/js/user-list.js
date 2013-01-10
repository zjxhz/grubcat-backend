$(function () {

    var $container = $('#user-container');
    $(".tags li").each(function () {
        if ($.inArray($(this).html(), tags) > -1) {
            $(this).addClass('common');
        }
    })
    $container.imagesLoaded(function () {
        $container.masonry({
            itemSelector:'.box',
            isAnimated:!Modernizr.csstransitions
//            animationOptions:{
//                duration:750,
//                easing:'linear',
//                queue:false
//            }
        });
    });

    var ajaxLoaderImageId = $("#ajax-load-image-id").attr('href');
    $container.infinitescroll({
            navSelector:'#page-nav', // selector for the paged navigation
            nextSelector:'#page-nav a', // selector for the NEXT link (to page 2)
            itemSelector:'.box', // selector for all items you'll retrieve
            animate:false,

//            speed:100,
//            debug:true,
            loading:{
                msgText:'加载中...',
                finishedMsg:'没有了！',
                img:ajaxLoaderImageId
            }
        },
        // trigger Masonry as a callback
        function (newElements) {
            // hide new items while they are loading
            var $newElems = $(newElements).css({ opacity:0 });
            // ensure that images load before adding to masonry layout
            $newElems.imagesLoaded(function () {
                // show elems now they're ready
                $newElems.animate({ opacity:1 });
                $container.masonry('appended', $newElems, true);
            });
            $(newElements).find(".tags li").each(function () {
                if ($.inArray($(this).html(), tags) > -1) {
                    $(this).addClass('common');
                }
            })
        }
    );

});