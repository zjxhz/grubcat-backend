from django_assets import Bundle, register, env

#css below
bootstrap_css = Bundle(
    'less/bootstrap/bootstrap.less', 'less/bootstrap/responsive.less', filters='less,cssmin',
    output='gen/bootstrap.%(version)s.css', depends='less/bootstrap/*.less'
)
bootstrap_ie6_css = Bundle(
    'less/bootstrap/bootstrap_ie6.less',filters='less,cssmin',
    output='gen/bootstrap.ie6.%(version)s.css', depends='less/bootstrap/*.less'
)
responsive_css = Bundle('less/responsive.less', filters='less,cssmin', output='gen/responsive.%(version)s.css')

base_css = Bundle(bootstrap_css, 'less/common.less', 'less/module.less', 'less/user.less', responsive_css,
                  filters='less,cssmin', output='gen/base.%(version)s.css')

base_restaurant_css = Bundle(bootstrap_css, 'css/jquery.Jcrop.css', 'less/common.less', 'less/restaurant_admin.less',
                             filters='less,cssmin', output='gen/restaurant.%(version)s.css')

#group related
#group_list_css = Bundle(
#     common_css, 'css/group_list.css', filters='cssmin', output='gen/group-list.%(version)s..css'
#)
#group_detail_css = Bundle(
#     common_css, 'css/group_detail.css', filters='cssmin', output='gen/group-detail.%(version)s.css'
#)

#user related

create_meal_css = Bundle(
    'less/bootstrap/datepicker.less', 'css/dropkick.css', 'css/lionbars.css', filters='less, cssmin', output='gen/create_meal.%(version)s.css'
)

edit_profile_css = Bundle(
    'css/jquery.Jcrop.css', 'less/autoSuggest.less', filters='less, cssmin', output='gen/edit_profile.%(version)s.css'
)


restaurant_admin_css = Bundle(
    'css/jquery.Jcrop.css', 'less/restaurant_admin.less', responsive_css, filters='less,cssmin',
    output='gen/restaurant-admin.%(version)s.css'
)

#js below
jquery_js = Bundle('js/jquery_1.7.2.js', output='gen/jquery-1.7.2.%(version)s.js', filters="yui_js")

jquery_dropkick_js = Bundle('js/jquery.dropkick_1.0.0.js', output='gen/jquery-dropkick.%(version)s.js', filters='yui_js')

jquery_color_js = Bundle('js/jquery.animate-colors-min.js', output='gen/jquery-color.%(version)s.js', filters='yui_js')

noty_js = Bundle('js/noty/jquery.noty.js', 'js/noty/layouts/top.js', 'js/noty/layouts/topCenter.js',
                 'js/noty/layouts/center.js', 'js/noty/themes/default.js',
                 output='gen/jquery-noty.%(version)s.js', filters='yui_js')

chat_js = Bundle('js/underscore_1.4.4.js', 'js/backbone_1.0.0.js', 'js/chat/iso8601_support.js',
                 'js/chat/strophe.js',
                 'js/chat/strophe.rsm.js', 'js/chat/strophe.chatstates.js', 'js/chat/strophe.archive.js',
                 'js/chat/strophe.roster.js', 'js/chat/strophe.messaging.js', 'js/chat/strophe.serverdate.js',
                 'js/chat/chat.js', filters='yui_js', output="gen/chat.%(version)s.js")

bootstrap_js = Bundle('js/bootstrap.js', filters='yui_js', output="gen/bootstrap.%(version)s.js")

bootstrap_box_js = Bundle('js/bootstrap_box.js', filters='yui_js', output="gen/bootstrap-box.%(version)s.js")

base_js = Bundle(jquery_js, 'js/utils.js',  bootstrap_js, noty_js, 'js/common.js', filters='yui_js',
                 output="gen/base.%(version)s.js")

base_main_js = Bundle(jquery_js, 'js/utils.js',  bootstrap_js, 'js/jquery.lazyload.js', 'js/common.js', filters='yui_js',
                      output="gen/base.main.%(version)s.js")

module_js = Bundle('js/module.js', filters='yui_js', output="gen/module.%(version)s.js")


water_fall_js = Bundle(
    'js/jquery.infinitescroll.js', 'js/jquery.masonry.js','js/jquery.lazyload.js',
    filters='yui_js', output='gen/water-fall.%(version)s.js'
)
jquery_form_js = Bundle('js/jquery.form.js', filters='yui_js', output='gen/jquery.form.%(version)s.js')

validate_js = Bundle('js/jqBootstrapValidation.js', filters='yui_js', output='gen/validate.%(version)s.js')

restaurant_admin_js = Bundle(
    bootstrap_box_js, 'js/restaurant_admin.js', filters='yui_js', output='gen/restaurant-admin.%(version)s.js'
)

edit_or_bind_profile_js = Bundle('js/jquery.autoSuggest.js', jquery_form_js, validate_js, filters='yui_js',
                                 output="gen/edit_profile.%(version)s.js")


create_meal_js = Bundle('js/bootstrap_datepicker.js', 'js/jquery.lionbars.0.3.js', jquery_dropkick_js,
                        validate_js, 'js/gmap3.v5.0b.min.js', filters='yui_js',
                        output="gen/create-meal.%(version)s.js")

jquery_ui_js = Bundle('js/jquery_ui_1.8.21.custom.js', filters='yui_js',
                      output='gen/jquery-ui-1.8.21.custom.%(version)s.js')

image_cropping_js = Bundle('js/jquery.Jcrop.js', 'js/image_cropping.js', filters='yui_js',
                           output='gen/iamge-cropping.%(version)s.js')

register('base_css', base_css)
register('base_restaurant_css', base_restaurant_css)
register('bootstrap_css', bootstrap_css)
register('bootstrap_ie6_css', bootstrap_ie6_css)
#register('group_list_css', group_list_css)
#register('group_detail_css', group_detail_css)

register('create_meal_css', create_meal_css)
register('edit_profile_css', edit_profile_css)
register('restaurant_admin_css', restaurant_admin_css)

register('bootstrap_js', bootstrap_js)
register('bootstrap_box_js', bootstrap_box_js)
register('jquery_js', jquery_js)
register('jquery_dropkick_js', jquery_dropkick_js)
register('jquery_color_js', jquery_color_js)
register('noty_js', noty_js)
register('base_js', base_js)
register('base_main_js', base_main_js)
register('module_js', module_js)
register('chat_js', chat_js)
register('create_meal_js', create_meal_js)
register('edit_or_bind_profile_js', edit_or_bind_profile_js)
register('restaurant_admin_js', restaurant_admin_js)
register('water_fall_js', water_fall_js)
register('jquery_form_js', jquery_form_js)
register('jquery_ui_js', jquery_ui_js)
register('image_cropping_js', image_cropping_js)

