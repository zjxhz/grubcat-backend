#coding=utf-8
from django import forms
from django.forms import ModelForm
from django.forms.widgets import *
from grubcat.eo.models import *


class MealForm(ModelForm):
    time = forms.SplitDateTimeField(input_date_formats='yyyy-MM-dd',input_time_formats='HH:mm')
    class Meta:
        model = Meal
        fields = ('time','region','topic','introduction','min_persons','list_price','extra_requests')
        widgets = {
            'introduction': Textarea(),
            'extra_requests':Textarea(),
        }


NUM_PERSON_CHOICE = [(x, "%s人" % x) for x in range(1, 10)]

class OrderCreateForm(ModelForm):
    meal_id = forms.CharField(widget=HiddenInput)

    def clean(self):
        return super(OrderCreateForm, self).clean()
        #TODO check if the user can add the meal order; private/already have one

    class Meta:
        model = Order
        fields = ('num_persons',)
        widgets = {
            'num_persons': Select(choices=NUM_PERSON_CHOICE, ),
            }


class DishForm(ModelForm):

    def __init__(self, restaurant=None, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = DishCategory.objects.filter(Q(restaurant=restaurant) | Q(restaurant__isnull=True))
        self.fields['categories'].help_text = ''

    class Meta:
        model = Dish
        exclude=("restaurant","menu")

class DishCategoryForm(ModelForm):
    class Meta:
        model = DishCategory

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields  = ('num_persons','average_price') # TODO 'photo'


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    file = forms.FileField()

class ImgTestForm(ModelForm):
    class Meta:
        model = ImageTest

#restaurant admin related
class OrderCheckInForm(forms.Form):
    code = forms.CharField(max_length=20, widget=(TextInput(attrs={'placeholder': "请输入用户就餐验证码"})))

