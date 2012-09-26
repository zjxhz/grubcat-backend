#coding=utf-8
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.timezone import now
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from eo.models import Dish, Order
from eo.forms import *
from eo.view_utils import *
import simplejson

#restaurant admin related views
class OrderCheckInView(FormView):
    template_name = "restaurant/checkin.html"
    form_class = OrderCheckInForm

    def form_valid(self, form):
        code = form.cleaned_data['code']
        order = Order.objects.filter(code=code)

        #TODO uncomment this below
        if order:
            order = order[0]
            #        if order and order[0].meal.restaurant == self.request.user.restaurant:
        #            order = order[0]
        #        else:
        #            order = None
        return render_to_response("restaurant/checkin_result.html", {'order': order})


def use_order(request):
    '''用户就餐时，餐厅管理员标记订单为已使用'''
    if request.method == 'POST':
        code = request.POST.get('code')
        order_id = request.POST.get('id')
        order = Order.objects.get(id=order_id, code=code)
        order.completed_time = now()
        order.status = OrderStatus.USED
        order.save()
        return createSucessJsonResponse('使用订单成功')


def add_dish_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        result = DishCategory.objects.get_or_create(name=category_name)
        category = result[0]
        created = result[1]
        if created:
            category.restaurant_id = request.user.restaurant.id
            category.save()
        return createSucessJsonResponse('成功', {'id': category.id, 'name': category.name, 'created': created})


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

    def get_object(self):
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
        return Menu.objects.filter(restaurant=self.request.user.restaurant, status=MenuStatus.PUBLISHED)


def add_edit_menu(request, pk=None):
    '''添加或者删除一个套餐，如果传入pk则是编辑，否则是添加'''
    if request.method == 'POST':
        menu_json = simplejson.loads(request.raw_post_data)
        num_persons = menu_json['num_persons']
        average_price = menu_json['average_price']
        menu_form = MenuForm({'num_persons': num_persons, 'average_price': average_price})
        if not menu_form.is_valid():
            return createGeneralResponse(ERROR, menu_form.errors, extra_dict={'url': reverse('restaurant_menu_list'), })
        menu = Menu(restaurant=request.user.restaurant, num_persons=num_persons, average_price=average_price)
        menu.save()

        items = menu_json['items']
        for order_no, item in enumerate(items):
            if 'num' in item:
                #dish
                dish = Dish(id=item['id'])
                dish_item = DishItem(menu=menu, dish=dish, num=item['num'],order_no=order_no+1 ) #start from 1
                dish_item.save()
            else:
                #category
                dish_category = DishCategory(id=item['id'])
                category_item = DishCategoryItem(menu=menu, category=dish_category, order_no=order_no+1 )
                category_item.save()
        return createSucessJsonResponse(u'保存套餐成功', extra_dict={'url': reverse('restaurant_menu_list'), })
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
    return add_edit_menu(request, None)


def edit_menu(request, pk):
    return add_edit_menu(request, pk)


def del_menu(request, pk):
    if request.method == 'POST':
        try:
            menu = Menu.objects.get(pk=pk)
            menu.status = MenuStatus.DELETED
            menu.save()
        except ObjectDoesNotExist:
            pass
    return createSucessJsonResponse(extra_dict={'url': reverse('restaurant_menu_list'), })
