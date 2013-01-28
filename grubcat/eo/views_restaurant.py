#coding=utf-8
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.timezone import now
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from eo.models import Dish, Order
from eo.forms import *
import simplejson

#restaurant admin related views
from eo.views_common import create_sucess_json_response, create_failure_json_response

class OrderCheckInView(FormView):
    template_name = "restaurant/checkin.html"
    form_class = OrderCheckInForm

    def form_valid(self, form):
        code = form.cleaned_data['code']
        order = Order.objects.filter(code=code)
        order.select_related('meal')
        data = {}
        #TODO uncomment this below
        if order:
            order = order[0]
            data = get_meal_info(order.meal)
            data['order'] = order
            data['is_passed'] = order.meal.start_date + timedelta(days=1) <= date.today()
            data['is_upcomming'] = order.meal.start_date - timedelta(days=1) >= date.today()
        return render_to_response("restaurant/checkin_result.html", data)


def get_meal_info(meal):
    is_today = meal.start_date == date.today()
    checked_persons = 0
    useful_orders = Order.objects.filter(status__in=(OrderStatus.CREATED, OrderStatus.PAYIED, OrderStatus.USED),
        meal=meal)
    #TODO remove created orders after alipay is implemented
    for o in useful_orders:
        if o.status == OrderStatus.USED:
            checked_persons += o.num_persons
    return {'is_today': is_today, 'checked_persons': checked_persons,
            'unchecked_persons': meal.actual_persons - checked_persons}


def use_order(request):
    '''用户就餐时，餐厅管理员标记订单为已使用'''
    if request.method == 'POST':
        #TODO check is mine
        code = request.POST.get('code')
        order_id = request.POST.get('id')
        order = Order.objects.get(id=order_id, code=code)
        order.completed_time = now()
        order.status = OrderStatus.USED
        order.save()
        data = get_meal_info(order.meal)
        data['order'] = order
        return render_to_response("restaurant/checkin_result.html", data)


class TodayMealListView(ListView):
    template_name = 'restaurant/today_meal_list.html'
    context_object_name = 'meal_list'

    def get_queryset(self):
        return Meal.objects.filter(restaurant=self.request.user.restaurant, start_date=date.today()).order_by(
            'start_time').select_related("menu")

    def get_context_data(self, **kwargs):
        for meal in self.object_list:
            checked_persons = 0
            useful_orders = Order.objects.filter(status__in=(OrderStatus.CREATED, OrderStatus.PAYIED, OrderStatus.USED),
                meal=meal)
            #TODO remove created orders after alipay is implemented
            for o in useful_orders:
                if o.status == OrderStatus.USED:
                    checked_persons += o.num_persons
            meal.checked_persons = checked_persons
            meal.unchecked_persons = meal.actual_persons - meal.checked_persons
            meal.total_price = meal.list_price * meal.actual_persons
        return super(TodayMealListView, self).get_context_data(**kwargs)


def add_dish_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        result = DishCategory.objects.get_or_create(name=category_name)
        category = result[0]
        created = result[1]
        if created:
            category.restaurant_id = request.user.restaurant.id
            category.save()
        return create_sucess_json_response('成功', {'id': category.id, 'name': category.name, 'created': created})


class DishListView(ListView):
    template_name = "restaurant/dish.html"
    context_object_name = "dish_list"

    def get_queryset(self):
        return Dish.objects.filter(restaurant=self.request.user.restaurant).prefetch_related('categories')


class DishCreateView(CreateView):
    form_class = DishForm
    template_name = "restaurant/add_edit_dish.html"
    success_url = reverse_lazy("restaurant_dish_list")

    def get_form_kwargs(self):
        kwargs = super(DishCreateView, self).get_form_kwargs()
        kwargs.update({"restaurant": self.request.user.restaurant})
        return kwargs

    def form_valid(self, form):
        dish = form.save(False)
        dish.restaurant = self.request.user.restaurant
        super(DishCreateView, self).form_valid(form)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('restaurant_dish_list')
        return HttpResponse(content=content)


class DishUpdateView(UpdateView):
    form_class = DishForm
    model = Dish
    template_name = "restaurant/add_edit_dish.html"
    success_url = reverse_lazy("restaurant_dish_list")

    def form_valid(self, form):
        super(DishUpdateView, self).form_valid(form)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('restaurant_dish_list')
        return HttpResponse(content=content)

    def get_form_kwargs(self):
        kwargs = super(DishUpdateView, self).get_form_kwargs()
        kwargs.update({"restaurant": self.request.user.restaurant})
        return kwargs


class DishDeleteView(DeleteView):
    model = Dish
    context_object_name = "dish"
    template_name = "restaurant/dish_confirm_delete.html"
    success_url = reverse_lazy("restaurant_dish_list")

    def get_object(self, queryset=None):
        dish = get_object_or_404(Dish, pk=self.kwargs['pk'],
            restaurant=self.request.user.restaurant)
        return dish

    def delete(self, request, *args, **kwargs):
        super(DishDeleteView, self).delete(request, *args, **kwargs)
        content = r'<a class="auto-close" href="%s"></a>' % reverse_lazy('restaurant_dish_list')
        return HttpResponse(content=content)


class MenuListView(ListView):
    template_name = "restaurant/menu_list.html"
    context_object_name = "menu_list"

    def get_queryset(self):
        return Menu.objects.filter(restaurant=self.request.user.restaurant, status=MenuStatus.PUBLISHED).order_by("created_time")

    def get_context_data(self, **kwargs):
        context = super(MenuListView,self).get_context_data( **kwargs)
        for menu in self.object_list:
            if not menu.photo:
                context['need_upload_cover'] = True
                break
        return context


class EditMenuCoverView(UpdateView):
    form_class = MenuCoverForm
    model = Menu
    context_object_name = "menu"
    template_name = "restaurant/crop_menu_cover.html"

    def get_success_url(self):
        return "/"

    def form_valid(self, form):
#        TODO check if mine
        super(EditMenuCoverView, self).form_valid(form)
        if self.request.GET.get('action') == 'upload':
            data = {'normal_cover_url': self.object.normal_cover_url}
        else:
            data = {'normal_cover_url': self.object.normal_cover_url}
        return create_sucess_json_response(extra_dict=data) #return text/html type, not json, hack for IE ajax upload file


def add_edit_menu(request, pk=None, is_copy=False):
    '''添加或者删除一个套餐，如果传入pk则是编辑，否则是添加'''
    if request.method == 'POST':
        menu_json = simplejson.loads(request.raw_post_data)
        num_persons = menu_json['num_persons']
        average_price = menu_json['average_price']
        name = menu_json['name']
        menu_form = MenuForm({'num_persons': num_persons, 'average_price': average_price, 'name': name})
        if not menu_form.is_valid():
            #TODO check
            return create_failure_json_response(menu_form.errors, extra_dict={'url': reverse('restaurant_menu_list'), })
        #TODO check if mine
        try:
            menu = Menu(restaurant=request.user.restaurant, num_persons=num_persons, average_price=average_price, name=name,)
            if pk:
                old_menu = Menu.objects.get(pk=pk)
                menu.created_time=old_menu.created_time
                if not is_copy:
                    old_menu.status = MenuStatus.DELETED
                    old_menu.name = "%s%s" % (old_menu.name, old_menu.id)
                    print old_menu.name
                    old_menu.save()
                    menu.photo=old_menu.photo
                    menu.cropping=old_menu.cropping
            menu.save()

        except IntegrityError:
            return create_failure_json_response(u'套餐名称已经存在，请重新输入一个',)

        items = menu_json['items']
        for order_no, item in enumerate(items):
            if 'num' in item:
                #dish
                dish = Dish(id=item['id'])
                dish_item = DishItem(menu=menu, dish=dish, num=item['num'], order_no=order_no + 1) #start from 1
                dish_item.save()
            else:
                #category
                dish_category = DishCategory(id=item['id'])
                category_item = DishCategoryItem(menu=menu, category=dish_category, order_no=order_no + 1)
                category_item.save()
        return create_sucess_json_response(u'保存套餐成功', extra_dict={'url': reverse('restaurant_menu_list'), })
    elif request.method == 'GET':
        categories = DishCategory.objects.filter(dish__restaurant=request.user.restaurant).order_by("-id").distinct()

        for cat in categories:
            cat.my_dishes = cat.dish_set.filter(restaurant=request.user.restaurant)

        dishes_with_no_category = Dish.objects.filter(restaurant=request.user.restaurant,
            categories__isnull=True).order_by("-id")
        categories_with_no_dish = DishCategory.objects.filter(Q(dish__isnull=True),
            Q(restaurant=request.user.restaurant) | Q(restaurant__isnull=True)
        ).order_by("-id")
        menu = None
        if pk:
            #edit menu
            try:
                menu = Menu.objects.get(pk=pk, restaurant=request.user.restaurant)
                if is_copy:
                    menu.name = ""
            except ObjectDoesNotExist:
                pass

        menu_form = MenuForm(instance=menu)
        category_form = DishCategoryForm()
    return render_to_response("restaurant/add_edit_menu.html",
        {'request': request, 'categories': categories, 'category_form': category_form,
         'dishes_with_no_category': dishes_with_no_category,
         'categories_with_no_dish': categories_with_no_dish,
         'menu': menu, 'menu_form': menu_form})


def add_menu(request):
    return add_edit_menu(request, None,is_copy=False)


def edit_menu(request, pk):
    return add_edit_menu(request, pk)

def copy_menu(request, pk):
    return add_edit_menu(request, pk, is_copy=True)

def del_menu(request, pk):
    if request.method == 'POST':
        try:
            menu = Menu.objects.get(pk=pk)
            menu.status = MenuStatus.DELETED
            menu.name = "%s%s" % (menu.name, menu.id)
            menu.save()
        except ObjectDoesNotExist:
            pass
    return create_sucess_json_response()
