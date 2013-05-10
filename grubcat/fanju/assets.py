from django_assets import Bundle, register, env

#css below
bootstrap_css = Bundle(
    'less/bootstrap/bootstrap.less', 'less/bootstrap/responsive.less', filters='less,cssmin',
    output='gen/bootstrap.%(version)s.css', depends='less/bootstrap/*.less'
)
dropkick_css = Bundle('css/dropkick.css', filters='cssmin', output='gen/dropkick.%(version)s.css')
common_css = Bundle(dropkick_css, 'less/common.less', filters='less,cssmin', output='gen/common.%(version)s.css')
responsive_css = Bundle('less/responsive.less', filters='less,cssmin', output='gen/responsive.%(version)s.css')

base_css = Bundle(bootstrap_css, 'css/lionbars.css', filters='cssmin', output='gen/base.%(version)s.css')

module_css = Bundle(
    common_css, 'less/module.less', responsive_css, filters='less,cssmin', output='gen/module.%(version)s.css'
)

error_css = Bundle(
    common_css, responsive_css, output='gen/error.%(version)s.css'
)

#group related
#group_list_css = Bundle(
#     common_css, 'css/group-list.css', filters='cssmin', output='gen/group-list.%(version)s..css'
#)
#group_detail_css = Bundle(
#     common_css, 'css/group-detail.css', filters='cssmin', output='gen/group-detail.%(version)s.css'
#)

#user related
account_css = Bundle(
    common_css, 'css/account.css', responsive_css, filters='cssmin', output='gen/account.%(version)s.css'
)

user_list_css = Bundle(
    common_css, 'less/user-list.less', responsive_css, filters='less, cssmin', output='gen/user-list.%(version)s.css'
)

user_css = Bundle(
    common_css, responsive_css, filters='cssmin', output='gen/user.%(version)s.css'
)

profile_css = Bundle(
    'css/jquery.Jcrop.css', 'less/autoSuggest.less', module_css,  'less/profile.less', responsive_css,
    filters='less,cssmin', output='gen/profile.%(version)s.css'
)

#order_css = Bundle(
#     common_css, 'css/order.css', filters='cssmin', output='gen/order.%(version)s.css'
#)

restaurant_admin_css = Bundle(
    'css/jquery.Jcrop.css', 'less/restaurant-admin.less', responsive_css, filters='less,cssmin',
    output='gen/restaurant-admin.%(version)s.css'
)

#js below
jquery_js = Bundle('js/jquery-1.7.2.js', output='gen/jquery-1.7.2.%(version)s.js', filters="yui_js")

jquery_dropkick_js = Bundle('js/jquery.dropkick-1.0.0.js', output='gen/jquery-dropkick.%(version)s.js', filters='yui_js')

noty_js = Bundle('js/noty/jquery.noty.js', 'js/noty/layouts/top.js', 'js/noty/layouts/topCenter.js',
                 'js/noty/layouts/center.js', 'js/noty/themes/default.js',
                 output='gen/jquery-noty.%(version)s.js', filters='yui_js')
# 'js/jquery.lionbars.0.3.js',
chat_js = Bundle('js/underscore-1.4.4.js', 'js/backbone-1.0.0.js', 'js/chat/iso8601_support.js',
                 'js/chat/strophe.js',
                 'js/chat/strophe.rsm.js', 'js/chat/strophe.chatstates.js', 'js/chat/strophe.archive.js',
                 'js/chat/strophe.roster.js', 'js/chat/strophe.messaging.js', 'js/chat/strophe.serverdate.js',
                 'js/chat/chat.js',
                 filters='yui_js',
                 output="gen/chat.%(version)s.js")
base_js = Bundle(jquery_js, 'js/utils.js',  'js/bootstrap.js', noty_js, filters='yui_js',
                 output="gen/base.%(version)s.js")

base_main_js = Bundle(jquery_js, 'js/utils.js',  'js/bootstrap.js', 'js/jquery.lazyload.js', filters='yui_js',
                      output="gen/base.main.%(version)s.js")

module_js = Bundle('js/module.js', filters='yui_js', output="gen/module.%(version)s.js")
auto_suggest_js = Bundle('js/jquery.autoSuggest.js', filters='yui_js', output="gen/autosuggest.%(version)s.js")

water_fall_js = Bundle(
    'js/jquery.infinitescroll.js', 'js/jquery.masonry.js', 'js/modernizr-transitions.js', filters='yui_js',
    output='gen/water-fall.%(version)s.js'
)
jquery_form_js = Bundle('js/jquery.form.js', filters='yui_js', output='gen/jquery.form.%(version)s.js')
validate_js = Bundle('js/jqBootstrapValidation.js', filters='yui_js', output='gen/validate.%(version)s.js')
restaurant_admin_js = Bundle(
    'js/restaurant-admin.js', filters='yui_js', output='gen/restaurant-admin.%(version)s.js'
)
create_meal_js = Bundle('js/bootstrap/bootstrap-datepicker.js', 'js/jquery.lionbars.0.3.js', jquery_dropkick_js,
                        validate_js, 'js/gmap3.v5.0b.min.js', filters='yui_js',
                        output="gen/create-meal.%(version)s.js")

jquery_ajax_bootstrap_js = Bundle(
    'js/jquery.controls.js', 'js/jquery.dialog2.js', 'js/jquery.dialog2.helpers.js', filters='yui_js',
    output='gen/jquery.ajax.bootstrap.%(version)s.js'
)

jquery_ui_js = Bundle('js/jquery-ui-1.8.21.custom.js', filters='yui_js',
                      output='gen/jquery-ui-1.8.21.custom.%(version)s.js')

image_cropping_js = Bundle('js/jquery.Jcrop.js', 'js/image_cropping.js', filters='yui_js',
                           output='gen/iamge-cropping.%(version)s.js')

register('common_css', common_css)
register('base_css', base_css)
register('bootstrap_css', bootstrap_css)
register('dropkick_css', dropkick_css)
register('module_css', module_css)
#register('group_list_css', group_list_css)
#register('group_detail_css', group_detail_css)

register('error_css', error_css)
register('account_css', account_css)
register('user_list_css', user_list_css)
register('profile_css', profile_css)
#register('order_css', order_css)
register('restaurant_admin_css', restaurant_admin_css)

register('jquery_js', jquery_js)
register('jquery_dropkick_js', jquery_dropkick_js)
register('noty_js', noty_js)
register('base_js', base_js)
register('base_main_js', base_main_js)
register('module_js', module_js)
register('chat_js', chat_js)
register('create_meal_js', create_meal_js)
register('auto_suggest_js', auto_suggest_js)
register('restaurant_admin_js', restaurant_admin_js)
register('water_fall_js', water_fall_js)
register('jquery_form_js', jquery_form_js)
register('validate_js', validate_js)
register('jquery_ajax_bootstrap_js', jquery_ajax_bootstrap_js)
register('jquery_ui_js', jquery_ui_js)
register('image_cropping_js', image_cropping_js)
