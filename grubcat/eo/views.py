#coding=utf-8
# Create your views here.
from datetime import datetime
import logging
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
import weibo
from eo.exceptions import NoRightException
from eo.models import   Order,\
    Relationship, Meal
from eo.views_common import  create_sucess_json_response, create_failure_json_response, create_no_right_response, SUCESS
from grubcat.eo.forms import *
import simplejson
from django.conf import settings


logger = logging.getLogger()
###Photo related views ###
class PhotoCreateView(CreateView):
    form_class = PhotoForm
    template_name = 'profile/photo/upload_photo.html'

    def form_valid(self, form):
        photo = form.save(False)
        photo.user = self.request.user.get_profile()
        super(PhotoCreateView, self).form_valid(form)
        data = {'status': SUCESS, 'redirect_url': reverse('photo_detail', kwargs={'pk': photo.id})}
        return HttpResponse(simplejson.dumps(data), ) #text/html hack for IE ajax upload file

    def get_context_data(self, **kwargs):
        context = super(PhotoCreateView, self).get_context_data(**kwargs)
        context['profile'] = self.request.user.get_profile()
        context['is_mine'] = True
        context['orders'] = context['profile'].orders.exclude(status=OrderStatus.CANCELED)
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
        context['is_mine'] = context['profile'] == self.request.user.get_profile()
        context['orders'] = context['profile'].orders.exclude(status=OrderStatus.CANCELED)
        return context


class PhotoListView(ListView):
    model = UserPhoto
    context_object_name = 'photo_list'
    template_name = 'profile/photo/photo_list.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        context['profile'] = UserProfile.objects.get(pk=self.kwargs['user_id'])
        context['is_mine'] = context['profile'] == self.request.user.get_profile()
        context['orders'] = context['profile'].orders.exclude(status=OrderStatus.CANCELED)
        return context

    def get_queryset(self):
        return UserPhoto.objects.filter(user__id=self.kwargs.get('user_id'))


def del_photo(request, pk):
    if request.method == 'POST':
        photo = UserPhoto.objects.get(pk=pk)
        if photo.user == request.user.get_profile():
            photo.delete()
            return create_sucess_json_response(u'成功删除照片！',
                {'redirect_url': reverse('photo_list', kwargs={'user_id': request.user.get_profile().id})})
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
        qs = Menu.objects.filter(status=MenuStatus.PUBLISHED, num_persons=num_persons).select_related('restaurant', )
        if hasattr(self.request.user, 'restaurant'):
            #餐厅用户只显示本餐厅的菜单
            qs = Menu.objects.filter(restaurant=self.request.user.restaurant, status=MenuStatus.PUBLISHED,
                num_persons=num_persons).select_related('restaurant', )
        return qs

class MenuDetailView(DetailView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'meal/menu_detail.html'

### Meal related views ###
class MealCreateView(CreateView):
    form_class = MealForm
    initial = {'start_date':date.today() + timedelta(days=4)}
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
        meal.host = self.request.user.get_profile()
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
    queryset = Meal.get_default_upcomming_meals()
    template_name = "meal/meal_list.html"
    context_object_name = "meal_list"
    #TODO add filter to queyset

    ### group related views ###


class GroupListView(ListView):
#    TODO order by member num
    queryset = Group.objects.filter(privacy=GroupPrivacy.PUBLIC).select_related('category').annotate(
        num_members=Count('members')).order_by('-num_members')
    template_name = "group/group_list.html"
    context_object_name = "group_list"

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['categories'] = GroupCategory.objects.all()
        return context


class GroupCreateView(CreateView):
    form_class = GroupForm
    template_name = 'group/add_group.html'

    def form_valid(self, form):
        group = form.save(False)
        group.owner = self.request.user
        super(GroupCreateView, self).form_valid(form)
        group.members.add(self.request.user)
        #        TODO need save many to many?
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('group_detail', kwargs={'pk': group.id})
        return HttpResponse(content=content)


class GroupUpdateView(UpdateView):
    form_class = GroupForm
    model = Group
    template_name = "group/edit_group.html"


class GroupLogoUpdateView(UpdateView):
    form_class = GroupLogoForm
    model = Group
    template_name = "group/edit_group_logo.html"

    def form_valid(self, form):
        group = form.save(False)
        super(GroupLogoUpdateView, self).form_valid(form)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('group_detail', kwargs={'pk': group.id})
        return HttpResponse(content=content)

GROUP_COMMENT_PAGINATE_BY = 5

class GroupDetailView(DetailView):
    model = Group
    context_object_name = "group"
    template_name = "group/group_detail.html"

    def get_queryset(self):
        return Group.objects.prefetch_related('comments__from_person', 'comments__replies__from_person')

    def get_context_data(self, **kwargs):
        parent_comments = GroupComment.objects.filter(parent__isnull=True, group=self.get_object()).select_related(
            'group',
            'from_person__user').prefetch_related('replies__from_person__user').order_by('-id')
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context.update({
            "parent_comments": parent_comments[:GROUP_COMMENT_PAGINATE_BY],
            'has_next': parent_comments.count() > GROUP_COMMENT_PAGINATE_BY
        })
        return context


class GroupCommentListView(ListView):
    template_name = "group/comment_list.html"
    context_object_name = "parent_comments"
    model = GroupComment
    paginate_by = GROUP_COMMENT_PAGINATE_BY

    def get_queryset(self):
        parent_comments = GroupComment.objects.filter(parent__isnull=True,
            group=self.kwargs['group_id']).select_related(
            'from_person__user').prefetch_related('replies__from_person__user').order_by('-id')
        return parent_comments

    def get_context_data(self, **kwargs):
        context = super(GroupCommentListView, self).get_context_data(**kwargs)
        context.update({
            "group_id": self.kwargs['group_id']
        })
        return context


class GroupMemberListView(ListView):
    template_name = "group/member_list.html"
    context_object_name = "user_list"
    paginate_by = 10

    def get_queryset(self):
        return  Group.objects.get(pk=self.kwargs['group_id']).members.all()

    def get_context_data(self, **kwargs):
        context = super(GroupMemberListView, self).get_context_data(**kwargs)
        context.update({
            "group_id": self.kwargs['group_id']
        })
        return context


def join_group(request, pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=pk)
        if group.privacy == GroupPrivacy.PUBLIC:
            #TODO refactor
            if request.user not in group.members.all():
                group.members.add(request.user)
                return create_sucess_json_response(u'已经成功加入该圈子！', {'redirect_url': reverse('group_list')})
            else:
                return create_failure_json_response(u'对不起您已经加入该圈子，无需再次加入！')
        else:
        #            need to handle invitation
            return create_no_right_response(u'对不起，只有受到邀请的用户才可以加入该私密圈子')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')


def leave_group(request, pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=pk)
        if request.user in group.members.all():
            group.members.remove(request.user)
            return create_sucess_json_response(u'已经成功离开该圈子！')
        else:
            return create_failure_json_response(u'对不起您还未加入该圈子！')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')


def create_group_comment(request):
    if request.method == 'POST':
        form = GroupCommentForm(request.POST)
        #TODO some checks
        if form.is_valid():
            comment = form.save()
            t = render_to_response('group/single_comment.html', {'comment': comment},
                context_instance=RequestContext(request))
            return create_sucess_json_response(u'已经成功创建评论！', {'comment_html': t.content})
        else:
            return create_failure_json_response(u'对不起您还未加入该圈子！')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')


def del_group_comment(request, pk):
    if request.method == 'POST':
        user_id = request.user.get_profile().id
        comment = GroupComment.objects.filter(pk=pk)
        #TODO some checks
        if len(comment) == 1:
            comment[0].delete()
        return create_sucess_json_response(u'已经成功删除评论！')
    elif request.method == 'GET':
        return HttpResponse(u'不支持该操作')

### User related views ###

#User related
class UploadAvatarView(UpdateView):
    form_class = UploadAvatarForm
    model = UserProfile
    template_name = "user/upload_avatar.html"

    def get_object(self, queryset=None):
        return self.request.user.get_profile()

    def get_success_url(self):
        return reverse('upload_avatar')

    def form_valid(self, form):
        super(UploadAvatarView, self).form_valid(form)
        if self.request.GET.get('action') == 'upload':
            return HttpResponseRedirect(reverse('upload_avatar'))
        else:
            data = {'big_avatar_url': self.object.big_avatar}
            return HttpResponse(simplejson.dumps(data)) #return text/html type, not json, hack for IE ajax upload file


class ProfileUpdateView(UpdateView):
    form_class = BasicProfileForm
    model = UserProfile
    template_name = 'user/edit-profile.html'

    def get_object(self, queryset=None):
        return self.request.user.get_profile()

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk':self.object.id})

class ProfileDetailView(DetailView):
    model = UserProfile
    context_object_name = 'profile'
    template_name = 'profile/basic_info.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['is_mine'] = self.object == self.request.user.get_profile()
        context['orders'] = context['profile'].orders.exclude(status=OrderStatus.CANCELED)
        if self.object.industry:
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

# not used for now
#class RegisterView(CreateView):
#    form_class = UserCreationForm
#    template_name = 'registration/register.html'
#
#    def get_context_data(self, **kwargs):
#        context = super(RegisterView, self).get_context_data(**kwargs)
#        context['next'] = self.get_success_url()
#        return context
#
#    def form_valid(self, form):
#        response = super(RegisterView, self).form_valid(form)
#        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
#        login(self.request, user)
#        return response
#
#    def get_success_url(self):
#        success_url = self.request.REQUEST.get('next', '')
#        netloc = urlparse.urlparse(success_url)[1]
#        # Use default setting if redirect_to is empty
#        if not success_url:
#            success_url = reverse_lazy("index")
#        # Heavier security check -- don't allow redirection to a different host.
#        elif netloc and netloc != self.request.get_host():
#            success_url = reverse_lazy("index")
#        return success_url


class UserListView(ListView):
#    queryset = UserProfile.objects.all().select_related('tags')
    template_name = "user/user_list.html"
    context_object_name = "user_list"
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('show') == 'common' and self.request.user.is_authenticated():
            return self.request.user.get_profile().tags.similar_objects()
        else:
            return UserProfile.objects.exclude(avatar="").exclude(
                user__restaurant__isnull=False).select_related('tags').order_by(
                '-id')

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated():
            if not user.get_profile().tags.all():
                context['need_edit_tags'] = True
            if not user.get_profile().avatar:
                context['need_upload_avatar'] = True
            if self.request.GET.get('show') != 'common':
                context['show_common_tags_link'] = True
            elif user.get_profile().tags.all() and not context['page_obj'].has_next() and context['page_obj'].number < 4:
                context['need_edit_tags_again'] = True
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
        order = form.save(False)
        order.customer = self.request.user.get_profile()
        order.meal_id = form.cleaned_data['meal_id']
        order.status = OrderStatus.PAYIED #TODO if alipay is used, here should be created status
        order.total_price = order.meal.list_price * order.num_persons
        #        TODO some checks
        response = super(OrderCreateView, self).form_valid(form)
        meal = order.meal
        if order.customer == meal.host:
            #创建饭聚后，支付
            if meal.status is MealStatus.CREATED_NO_MENU:
                meal.status = MealStatus.PAID_NO_MENU
            elif meal.status is MealStatus.CREATED_WITH_MENU:
                meal.status = MealStatus.PUBLISHED
        order.meal.join(order)
        return response


class MealDetailView(OrderCreateView):
    form_class = OrderCreateForm
    template_name = "meal/meal_detail.html"

    def get_context_data(self, **kwargs):
        context = super(MealDetailView, self).get_context_data(**kwargs)
        meal = Meal.objects.select_related('menu__restaurant', 'host__user').prefetch_related('participants__user').get(
            pk=self.kwargs.get('meal_id'))
        context['meal'] = meal
        context['avaliable_seats'] = range(meal.left_persons)
        if self.request.user.is_authenticated() and self.request.user.get_profile() in meal.participants.all():
            orders = Order.objects.filter(meal=meal,
                customer=self.request.user.get_profile()) #TODO , status=OrderStatus.PAYIED
            if orders.exists():
                context['order'] = orders[0]
        if self.request.user.is_authenticated() and self.request.user.get_profile() == meal.host and meal.status == MealStatus.CREATED_WITH_MENU:
            context['just_created'] = True
        return context


class OrderDetailView(DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order/order_detail.html"
    queryset = Order.objects.select_related('meal__menu__restaurant')

    def get_object(self, queryset=None):
        order = super(OrderDetailView, self).get_object()
        if order.customer != self.request.user.get_profile():
            raise NoRightException
        return order


class UserMealListView(TemplateView):
    template_name = "profile/meals.html"

    def get_context_data(self, **kwargs):
        context = super(UserMealListView, self).get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.kwargs['user_id'])
        orders = user.orders.exclude(
            status=OrderStatus.CANCELED).order_by("meal__start_date", "meal__start_time").select_related('meal')
        context['upcomming_orders'] = orders.filter(
            Q(meal__start_date__gt=date.today()) | Q(meal__start_date=date.today(),
                meal__start_time__gt=datetime.now().time()))

        context['passed_orders'] = orders.filter(
            Q(meal__start_date__lt=date.today()) | Q(meal__start_date=date.today(),
                meal__start_time__lt=datetime.now().time())).order_by("-meal__start_date", "-meal__start_time")

        context['profile'] = user
        context['is_mine'] = user == self.request.user.get_profile()
        context['orders'] = context['profile'].orders.exclude(status=OrderStatus.CANCELED)
        return context


def weibo_login(request):
    weibo_client = weibo.APIClient(app_key=settings.WEIBO_APP_KEY, app_secret=settings.WEIBO_APP_SECERT,
        redirect_uri=settings.WEIBO_REDIRECT_URL)

#    if request.user.is_authenticated() and not request.user.is_active:
#        return HttpResponseRedirect(reverse_lazy('bind'))

    code = request.GET.get('code')
    errorcode = request.GET.get('error_code')
    next = request.GET.get('state', '/')
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
        except:
            raise Exception(u'微博接口异常')
            #        data = {'access_token':'2.00xQDpnBG_tW8E7a7387b8510f3_eq'} #for local debug
        user_to_authenticate = auth.authenticate(**data)
        if user_to_authenticate:
            auth.login(request, user_to_authenticate)
#            if not request.user.is_active:
#                return HttpResponseRedirect(reverse_lazy('bind') + '?next=' + next)
#            else:
            return HttpResponseRedirect(next)
        else:
            raise Exception(u'微博接口异常')


#class BindProfileView(UpdateView):
#    form_class = BindProfileForm
#    model = UserProfile
#    template_name = 'user/bind_profile.html'
#
#    def get_object(self, queryset=None):
#        return self.request.user.get_profile()
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
        follower = request.user.get_profile()
        followee = UserProfile.objects.get(id=user_id)
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
            user_to_be_unfollowed = UserProfile.objects.get(id=user_id)
            relationship = Relationship.objects.get(from_person=request.user.get_profile(), to_person=user_to_be_unfollowed)
            relationship.delete()
            html = '<a class="btn btn-follow" href="%s"><i class="icon-star"></i> 关注</a>' % (
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
        context['profile'] = self.request.user.get_profile()
        context['is_mine'] = True
        context['orders'] = context['profile'].orders.exclude(status=OrderStatus.CANCELED)
        return context

#others
def handle_uploaded_app(file):
    destination = open(settings.MEDIA_ROOT + '/apps/' + file.name, 'wb+')
    for chunk in file.chunks():
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

