#coding=utf-8
import logging
import xml.dom.minidom
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
import weibo
from fanju.exceptions import *
from fanju.models import Order, Relationship, Meal
from fanju.pay.alipay.alipay import create_direct_pay, verify_sign, decrypt, create_wap_pay
from fanju.pay.alipay.config import settings as alipay_settings
from fanju.util import isMobileRequest
from fanju.views_common import create_sucess_json_response, create_failure_json_response, create_no_right_response, SUCESS, handle_alipay_back
from fanju.forms import *
from django.conf import settings
from datetime import datetime, date, timedelta
import json

logger = logging.getLogger(__name__)
pay_logger = logging.getLogger("fanju.pay")

###Photo related views ###


class PhotoCreateView(CreateView):
    form_class = PhotoForm
    template_name = 'profile/photo/upload_photo.html'

    def form_valid(self, form):
        photo = form.save(False)
        photo.user = self.request.user
        super(PhotoCreateView, self).form_valid(form)
        data = {'status': SUCESS, 'redirect_url': reverse('photo_detail', kwargs={'pk': photo.id})}
        return HttpResponse(json.dumps(data), ) #text/html hack for IE ajax upload file

    def get_context_data(self, **kwargs):
        context = super(PhotoCreateView, self).get_context_data(**kwargs)
        context['profile'] = self.request.user
        set_profile_common_attrs(context, self.request)
        return context


class PhotoDetailView(DetailView):
    model = UserPhoto
    context_object_name = 'photo'
    template_name = 'profile/photo/photo_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        context['profile'] = self.object.user
        try:
            pre_photo = UserPhoto.objects.filter(user=self.object.user, id__lt=self.object.id).order_by('-id')[0]
        except IndexError:
            pre_photo = UserPhoto.objects.filter(user=self.object.user).order_by('-id')[0]
        try:
            next_photo = UserPhoto.objects.filter(user=self.object.user, id__gt=self.object.id).order_by('id')[0]
        except IndexError:
            next_photo = UserPhoto.objects.filter(user=self.object.user).order_by('id')[0]
        context['pre_photo'] = pre_photo
        context['next_photo'] = next_photo
        context['profile'] = self.object.user
        set_profile_common_attrs(context, self.request)
        return context


def set_profile_common_attrs(context, request):
    '''
    used in all profile pages:basic_profile, photo_list, photo_detail, upload_photo, user_meals, follower/followees
    '''
    context['is_mine'] = context['profile'] == request.user
    context['orders_count'] = context['profile'].orders.filter(status__in=(OrderStatus.PAYIED,OrderStatus.USED )).count()
    if context['is_mine']:
        context['orders_count'] += context['profile'].get_paying_orders_count()


class PhotoListView(ListView):
    model = UserPhoto
    context_object_name = 'photo_list'
    template_name = 'profile/photo/photo_list.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        context['profile'] = User.objects.get(pk=self.kwargs['user_id'])
        set_profile_common_attrs(context, self.request)
        return context

    def get_queryset(self):
        return UserPhoto.objects.filter(user__id=self.kwargs.get('user_id'))


def del_photo(request, pk):
    if request.method == 'POST':
        photo = UserPhoto.objects.get(pk=pk)
        if photo.user == request.user:
            photo.delete()
            return create_sucess_json_response(u'成功删除照片！',
                {'redirect_url': reverse('photo_list', kwargs={'user_id': request.user.id})})
        else:
            return create_no_right_response(u'对不起，只有照片的所有者才能删除该照片')
    elif request.method == 'GET':
        return HttpResponseRedirect(reverse('photo_detail', kwargs={'pk': pk}))


###Menu related views ###
class MenuListView(ListView):
    template_name = "meal/get_menus.html"
    context_object_name = "menu_list"

    def get_queryset(self):
        #TODO filter by  date and time
        num_persons = self.request.GET.get("num_persons", 8)
        qs = Menu.objects.filter(status=MenuStatus.PUBLISHED, num_persons=num_persons,).exclude(photo='').select_related('restaurant', )
        if hasattr(self.request.user, 'restaurant'):
            #餐厅用户只显示本餐厅的菜单
            qs = qs.filter(restaurant=self.request.user.restaurant)
        return qs


class MenuDetailView(DetailView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'meal/menu_detail.html'

### Meal related views ###
class MealCreateView(CreateView):
    form_class = MealForm
    initial = {'start_date': date.today() + timedelta(days=4)}
    template_name = 'meal/create_meal.html'

    #    def get_context_data(self, **kwargs):
    #        context = super(MealCreateView, self).get_context_data(**kwargs)
    #        context.update({
    #            "my_groups": self.request.user.interest_groups.all()
    #        })
    #        return context

    def get_success_url(self):
        if self.object.status == MealStatus.PUBLISHED:
            return super(MealCreateView, self).get_success_url()
        else:
        #普通用户发起饭聚后需要支付
            return reverse_lazy('meal_detail', kwargs={'meal_id': self.object.id})

    def form_valid(self, form):
        meal = form.save(False)
        meal.host = self.request.user
        meal.max_persons = meal.min_persons
        menu_id = form.cleaned_data['menu_id']
        if menu_id:
            meal.menu_id = menu_id
            meal.list_price = meal.menu.average_price
            meal.region = None
            #TODO to remove
            meal.restaurant = meal.menu.restaurant

        if hasattr(self.request.user, 'restaurant'):
            meal.status = MealStatus.PUBLISHED
        elif menu_id:
            meal.status = MealStatus.CREATED_WITH_MENU
        else:
            meal.status = MealStatus.CREATED_NO_MENU
        response = super(MealCreateView, self).form_valid(form)
        return response


class MealListView(ListView):
    template_name = "meal/meal_list.html"
    context_object_name = "meal_list"
    #TODO add filter to queyset
    def get_queryset(self):
        return Meal.get_default_upcomming_meals()


### User related views ###
def get_user_info(request):
    if request.method == 'POST':
        if request.POST.get("ids"):
            usernames = request.POST.get("ids").split(",")
            users = User.objects.filter(username__in=usernames)
            result = []
            for user in users:
                result.append({"id": user.username, "name": user.name, "avatarUrl": user.small_avatar,
                               'profileUrl': user.get_absolute_url()})
        elif request.POST.get("id"):
            username = request.POST.get("id")
            user = User.objects.filter(username=username)
            if len(user):
                user = user[0]
                result = {"id": user.username, "name": user.name, "avatarUrl": user.small_avatar,
                          'profileUrl': user.get_absolute_url()}
            else:
                result = {}
        return HttpResponse(json.dumps(result), content_type='application/json', )


#User related
class UploadAvatarView(UpdateView):
    form_class = UploadAvatarForm
    model = User
    template_name = "profile/upload_avatar.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('upload_avatar')

    def form_valid(self, form):
        super(UploadAvatarView, self).form_valid(form)
        if self.request.GET.get('action') == 'upload':
            return HttpResponseRedirect(reverse('upload_avatar'))
        else:
            data = {'big_avatar_url': self.object.big_avatar, 'small_avatar_url': self.object.small_avatar}
            return HttpResponse(json.dumps(data)) #return text/html type, not json, hack for IE ajax upload file


class ProfileUpdateView(UpdateView):
    form_class = BasicProfileForm
    model = User
    template_name = 'profile/edit_profile.html'

    def get_object(self, queryset=None):

        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['profile'] = self.request.user
        set_profile_common_attrs(context, self.request)
        return context

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.id})


class ProfileDetailView(DetailView):
    model = User
    context_object_name = 'profile'
    template_name = 'profile/basic_info.html'

    def get_context_data(self, **kwargs):

        from_user = self.request.user
        if from_user != self.object:
            Visitor.objects.get_or_create(from_person=from_user, to_person=self.object)

        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        set_profile_common_attrs(context, self.request)
        if self.object.industry >= 0:
            for industry_value, industry_label in INDUSTRY_CHOICE:
                if self.object.industry == industry_value:
                    context['industry_label'] = industry_label
                    break
        if self.object.gender is not None:
            for value, label in GENDER_CHOICE:
                if self.object.gender == value:
                    context['gender_label'] = label
                    break
        return context


class UserListView(ListView):
#    queryset = User.objects.all().select_related('tags')
    template_name = "profile/user_list.html"
    context_object_name = "user_list"
    paginate_by = 20

    def get_queryset(self):
        tags = self.request.GET.get('tags')
        users = User.objects.exclude(
            avatar__in=('', settings.DEFAULT_MALE_AVATAR, settings.DEFAULT_FEMALE_AVATAR)).exclude(
            restaurant__isnull=False).select_related('tags').order_by('-id')
        if self.request.GET.get('show') == 'common' and self.request.user.is_authenticated():
            return self.request.user.tags.similar_objects()
        elif tags:
            return users.filter(tags__name__in=(tags, )).distinct()
        else:
            return users

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user = self.request.user

        if context['page_obj'].has_next():
            next_page_url = reverse_lazy('more_user',kwargs={'page': context['page_obj'].next_page_number()})+"?"
            for arg in ('show', 'tags'):
                if self.request.GET.get(arg):
                    next_page_url += ("%s=%s&" % (arg, self.request.GET.get(arg)))
            context['next_page_url'] = next_page_url

        if user.is_authenticated():
            if not user.tags.all():
                context['need_edit_tags'] = True
            context['need_upload_avatar'] = user.is_default_avatar()
            if self.request.GET.get('show') != 'common':
                context['show_common_tags_link'] = True
            elif user.tags.all() and not context['page_obj'].has_next() and context['page_obj'].number < 4:
                context['need_edit_tags_again'] = True
            if self.request.GET.get('tags') and not self.request.user.tags.filter(name=self.request.GET.get('tags')).exists():
                context['show_add_tag'] = True
        return context


### Order related views ###
class OrderCreateView(CreateView):
    form_class = OrderCreateForm
    template_name = 'order/create_order.html'

    def get_initial(self):
        return {'meal_id': self.kwargs['meal_id']}

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        try:
            context['meal'] = Meal.objects.get(pk=self.kwargs['meal_id'])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(u'饭局不存在')
        return context

    def form_valid(self, form):
        meal = Meal.objects.get(pk=form.cleaned_data['meal_id'])
        num_persons = form.cleaned_data['num_persons']
        customer = self.request.user
        order = meal.join(customer, num_persons)
        #        TODO some checks
        if not settings.PAY_DEBUG:
            if isMobileRequest(self.request):
                url = create_wap_pay(order.id, order.meal.topic, meal.list_price, num_persons)
            else:
                url = create_direct_pay(order.id, order.meal.topic, meal.list_price, num_persons)
            pay_logger.info("支付订单：%s" % url)
        else:
            handle_alipay_back(order.id)
            url = order.get_absolute_url()
        return HttpResponseRedirect(url)

#TODO check pay status

class MealDetailView(OrderCreateView):
    form_class = OrderCreateForm
    template_name = "meal/meal_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        meal = Meal.objects.select_related('menu__restaurant', ).prefetch_related('participants').get(
            pk=self.kwargs.get('meal_id'))
        context['meal'] = meal
        context['avaliable_seats'] = range(meal.left_persons)

        payed_orders = Order.objects.filter(meal=meal, status__in=(OrderStatus.PAYIED, OrderStatus.USED))
        context['payed_orders'] = payed_orders

        if self.request.user.is_authenticated():
            my_orders = payed_orders.filter(customer=self.request.user)
            if len(my_orders) == 1 :
                context['order'] = my_orders[0]
            elif len(my_orders) > 1:
                logger.error('user %s has %s orders for meal %s' % (self.request.user.id, len(my_orders), meal.id ))

        if self.request.user.is_authenticated() and self.request.user == meal.host and meal.status == MealStatus.CREATED_WITH_MENU: #NO menu
            context['just_created'] = True
        else:
            context['just_created'] = False
        return context


def check_order_status(request, meal_id):
    if request.method == "POST":
        meal = Meal.objects.get(pk=meal_id)
        payed_orders = Order.objects.filter(meal=meal, status=OrderStatus.PAYIED, customer=request.user)
        if len(payed_orders):
            return create_sucess_json_response(extra_dict={'redirect_url': payed_orders[0].get_absolute_url()})
        elif meal.left_persons <= 0:
            return create_sucess_json_response(extra_dict={'redirect_url': meal.get_absolute_url()})
    return create_failure_json_response()


class OrderDetailView(DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order/order_detail.html"
    queryset = Order.objects.select_related('meal__menu__restaurant')

    def get_object(self, queryset=None):
        order = super(OrderDetailView, self).get_object()
        if order.customer != self.request.user:
            raise NoRightException
        return order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['avatar_tip'] = self.request.user.is_default_avatar()
        return context


#支付30分钟内未支付的饭局
def pay_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if order.customer != request.user:
        raise NoRightException
    url = "%s?num=%s" % (reverse('meal_detail', kwargs={'meal_id': order.meal.id}), order.num_persons)
    return HttpResponseRedirect(url)


class UserMealListView(TemplateView):
    template_name = "profile/meals.html"

    def get_context_data(self, **kwargs):
        context = super(UserMealListView, self).get_context_data(**kwargs)
        user = User.objects.get(pk=self.kwargs['user_id'])
        context['profile'] = user
        set_profile_common_attrs(context, self.request)
        if context['is_mine']:
            context['paying_orders'] = user.get_paying_orders()
            context['pay_overtime'] = settings.PAY_OVERTIME_FOR_PAY_OR_USER
        context['upcomming_orders'] = user.get_upcomming_orders()
        context['passed_orders'] = user.get_passed_orders()
        return context


def weibo_login(request):
    weibo_client = weibo.APIClient(app_key=settings.WEIBO_APP_KEY, app_secret=settings.WEIBO_APP_SECERT,
                                   redirect_uri=settings.WEIBO_REDIRECT_URL)

    #    if request.user.is_authenticated() and not request.user.is_active:
    #        return HttpResponseRedirect(reverse_lazy('bind'))

    code = request.GET.get('code')
    errorcode = request.GET.get('error_code')
    next_url = request.GET.get('state', '/')
    if not code and not errorcode:
        #go to weibo site to auth
        kw = {'state': request.GET.get('next', '/')}
        return HttpResponseRedirect(weibo_client.get_authorize_url(**kw))
    elif not code and errorcode:
        # when weibo auth, user cancel auth
        #TODO inform user to auth again
        return HttpResponseRedirect("/")
    else:
    #        after weibo auth
        try:
            data = weibo_client.request_access_token(code)
            logger.debug(data)
        except:
            raise Exception(u'对不起，现在是内测阶段未开放注册！')
            #        data = {'access_token':'2.00xQDpnBG_tW8E7a7387b8510f3_eq'} #for local debug
        user_to_authenticate = auth.authenticate(**data)
        if user_to_authenticate:
            auth.login(request, user_to_authenticate)
            #            if not request.user.is_active:
            #                return HttpResponseRedirect(reverse_lazy('bind') + '?next=' + next)
            #            else:
            return HttpResponseRedirect(next_url)
        else:
            # raise Exception(u'微博接口异常')
            raise Exception(u'对不起，现在是内测阶段未开放注册！')


#class BindProfileView(UpdateView):
#    form_class = BindProfileForm
#    model = User
#    template_name = 'user/bind_profile.html'
#
#    def get_object(self, queryset=None):
#        return self.request.user
#
#    def get_success_url(self):
#        success_url = self.request.GET.get('next', reverse('index'))
#        return success_url
#
#    def form_valid(self, form):
#        profile = form.save(False)
#        profile.user.is_active = True
#        profile.user.save()
#        return super(BindProfileView, self).form_valid(form)


def follow(request, user_id):
    if request.method == 'POST':
        follower = request.user
        followee = User.objects.get(id=user_id)
        try:
            follower.follow(followee)
            html = '<a class="btn btn-unfollow" href="%s">取消关注</a>' % (
                reverse('un_follow', kwargs={'user_id': followee.id}))
            return create_sucess_json_response(extra_dict={'html': html})
        except BusinessException as e:
            return create_failure_json_response(e.message)
    else:
        raise Exception("不支持该方法")


def un_follow(request, user_id):
    if request.method == 'POST':
        try:
            user_to_be_unfollowed = User.objects.get(id=user_id)
            relationship = Relationship.objects.get(from_person=request.user,
                                                    to_person=user_to_be_unfollowed)
            relationship.delete()
            html = u'<a class="btn btn-follow" data-uid="%s" href="%s"><i class="icon-star"></i> 关注</a>' % (
                user_to_be_unfollowed.username,
                reverse('follow', kwargs={'user_id': user_to_be_unfollowed.id}))
            return create_sucess_json_response(extra_dict={'html': html})
        except Exception:
            return create_failure_json_response("你没有关注TA")
    else:
        raise Exception("不支持该方法")


class FollowsView(TemplateView):
    template_name = 'profile/follow_list.html'

    def get_context_data(self, **kwargs):
        context = super(FollowsView, self).get_context_data(**kwargs)
        context['profile'] = self.request.user
        set_profile_common_attrs(context, self.request)
        return context


#others
def handle_uploaded_app(app_file):
    destination = open(settings.MEDIA_ROOT + '/apps/' + app_file.name, 'wb+')
    for chunk in app_file.chunks():
        destination.write(chunk)
    destination.close()


def upload_app(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        handle_uploaded_app(request.FILES['file'])
        return create_sucess_json_response()
    else:
        form = UploadFileForm()
    return render_to_response('test/upload.html', {'form': form})

############### pays

order_prefix = getattr(settings, 'ORDER_PREFIX', '')


def handle_alipay_wap_async_back(request):
    data = request.POST
    pay_logger.info(u'alipay_wap异步通知--开始....')
    pay_logger.info(data)
    try:
        #支付宝wap异步返回验签的参数顺序为如下固定顺序
        notify_data = decrypt( smart_str(data.get('notify_data')))
        sort = ('service', 'v', 'sec_id', 'notify_data')
        result_param = {
            'service': data.get('service'),
            'v': data.get('v'),
            'sec_id': data.get('sec_id'),
            'notify_data': notify_data,
            'sign': data.get('sign')
        }
        verify_sign(result_param, sort=sort)

        #parse notify_data
        doc = xml.dom.minidom.parseString(notify_data)
        trade_status = doc.getElementsByTagName("trade_status")[0].firstChild.data
        alipay_trade_no = doc.getElementsByTagName("trade_no")[0].firstChild.data
        order_id = doc.getElementsByTagName("out_trade_no")[0].firstChild.data.replace(order_prefix, '')
        gmt_payment = doc.getElementsByTagName("gmt_payment")[0].firstChild.data

        pay_logger.debug(trade_status)
        if trade_status in ("TRADE_SUCCESS", 'TRADE_FINISHED'):
            handle_alipay_back(order_id, alipay_trade_no, gmt_payment)
    except AlreadyJoinedError:
        pass
    except Exception, e:
        pay_logger.error(u"alipay_wap异步通知--结束--失败 "+ unicode(e))
        return HttpResponse("fail")
    pay_logger.info(u"alipay_wap异步通知--结束--成功")
    return HttpResponse("success")
    #TRADE_FINISHED 直接返回success


def handle_alipay_wap_sync_back(request):
    data = request.GET
    trade_status = data.get('result')
    pay_logger.info(u'alipay_wap同步通知开始....' + trade_status)
    pay_logger.info(data)
    order_id = data.get('out_trade_no').replace(order_prefix, '')
    if data.get('result') == "success":
        verify_sign(data)
        handle_alipay_back(order_id, data.get('trade_no'))
        order = Order.objects.get(pk=order_id)
        pay_logger.info(u"alipay_wap同步通知--结束--成功")
        return HttpResponseRedirect(order.get_absolute_url())


def handle_alipay_direct_sync_back(request):
    data = request.GET
    trade_status = data.get('trade_status')
    pay_logger.info(u'alipay_web同步通知开始....' + trade_status)
    pay_logger.info(data)
    order_id = data.get('out_trade_no').replace(order_prefix, '')
    if trade_status in ('WAIT_SELLER_SEND_GOODS',   "TRADE_SUCCESS", 'success'):
        verify_sign(data, signType=alipay_settings.ALIPAY_DIRECT_SIGN_TYPE)
        handle_alipay_back(order_id, data.get('trade_no'), data.get('gmt_payment'))
        order = Order.objects.get(pk=order_id)
        pay_logger.info(u"alipay_web同步通知--结束--成功")
        return HttpResponseRedirect(order.get_absolute_url())


@csrf_exempt
def handle_alipay_direct_aysnc_back(request):
    data = request.POST
    trade_status = data.get('trade_status')
    pay_logger.info(u'alipay_web异步通知开始....' + trade_status)
    pay_logger.info(data)
    if trade_status in ('WAIT_SELLER_SEND_GOODS', "TRADE_SUCCESS"):
        #WAIT_SELLER_SEND_GOODS 是担保支付返回的成功状态，TRADE_SUCCESS是及时支付返回的成功状态
        try:
            verify_sign(data, signType=alipay_settings.ALIPAY_DIRECT_SIGN_TYPE )
            handle_alipay_back(data.get('out_trade_no').replace(order_prefix, ''), data.get('trade_no'),
                               data.get('gmt_payment'))
        except AlreadyJoinedError:
            pass
        except Exception, e:
            pay_logger.exception(u"alipay_web异步通知--结束--失败 " + unicode(e))
            return HttpResponse("fail")
    pay_logger.info(u"alipay_web异步通知--结束--成功")
    return HttpResponse("success")

@csrf_exempt
def handle_alipay_app_async_back(request):
    data = request.POST
    pay_logger.info(u'alipay_app异步通知--开始....')
    pay_logger.info(data)
    try:
        notify_data = smart_str(data.get('notify_data'))

        verify_sign("notify_data=%s" % notify_data, data.get('sign'))

        doc = xml.dom.minidom.parseString(notify_data)
        trade_status = getTextByTagName(doc, 'trade_status')
        pay_logger.debug(trade_status)
        if trade_status in('TRADE_FINISHED', 'TRADE_SUCCESS'):
            alipay_trade_no = getTextByTagName(doc, 'trade_no')
            order_id = getTextByTagName(doc, 'out_trade_no').replace(order_prefix,'')
            gmt_payment = getTextByTagName(doc, 'gmt_payment')
            handle_alipay_back(order_id, alipay_trade_no, gmt_payment, check_overtime=True)
    except (AlreadyJoinedError, PayOverTimeError):
        pass
    except Exception, e:
        pay_logger.exception(u"alipay_app异步通知--结束--失败 " )
        return HttpResponse("fail")
    pay_logger.info(u"alipay_app异步通知--结束--成功")
    return HttpResponse("success")


def getTextByTagName(doc, tag):
    tags = doc.getElementsByTagName(tag)
    if len(tags):
        return tags[0].firstChild.data
    else:
        return ""


def handle_alipay_app_sync_back(request):
    pay_logger.info(u'alipay_app同步通知开始....')
    data = request.POST
    pay_logger.info(data)
    try:
        alipay_result_str = data.get("alipay_result")
        sign = data.get('sign')
        alipay_result = alipay_result_str.split("&")
        params = {}
        verify_sign(alipay_result_str, sign)

        for p in alipay_result:
            index = p.index('=')
            params[p[:index]] = p[index + 2:-1]
        order_id = params.get('out_trade_no').replace(order_prefix, '')
        handle_alipay_back(order_id, check_overtime=True)
        order = Order.objects.get(pk=order_id)
        pay_logger.info(u"alipay_app同步通知--结束--成功")
        return create_sucess_json_response(extra_dict={'order_id': order_id, 'code': order.code})
    except (AlreadyJoinedError, PayOverTimeError), e:
        return create_failure_json_response(e.message)
    except Exception, e:
        pay_logger.exception('alipay_app sync bac error')
        return create_failure_json_response(u'对不起，支付出现了问题，请您查看是否已经支付成功')