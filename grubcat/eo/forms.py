#coding=utf-8
from django import forms
from django.forms import ModelForm
from django.forms.extras import SelectDateWidget
from django.forms.util import to_current_timezone
from django.forms.widgets import *
from image_cropping import ImageCropWidget
from grubcat.eo.models import *


class MealForm(ModelForm):
    menu_id = forms.CharField(widget=HiddenInput, required=False)

    #    def __init__(self, *args, **kwargs  ):
    #        super(MealForm, self).__init__(*args, **kwargs)
    #        interest_groups = kwargs.get('initial').get('request').user.interest_groups.all()
    #        if interest_groups:
    #            self.fields['group'].queryset = interest_groups
    #        else:
    #            del self.fields['group']


    class Meta:
        model = Meal
        fields = (
            'topic', 'introduction', 'start_date', 'start_time', 'region', 'min_persons', 'list_price',
            )
        widgets = {
            'introduction': Textarea({'rows': 5}),
            'extra_requests': Textarea({'rows': 5}),
        }

    def clean(self):
        cleaned_data = super(MealForm, self).clean()
        menu_id = cleaned_data.get("menu_id")
        if not menu_id:
            self._errors["menu_id"] = self.error_class([u'请您在左边选择一个套餐'])
        return cleaned_data


NUM_PERSON_CHOICE = [(x, "%s 人" % x) for x in range(1, 13)]

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
        self.fields['categories'].queryset = DishCategory.objects.filter(
            Q(restaurant=restaurant) | Q(restaurant__isnull=True))
        self.fields['categories'].help_text = ''

    class Meta:
        model = Dish
        exclude = ("restaurant", "menu")


class DishCategoryForm(ModelForm):
    class Meta:
        model = DishCategory


class GroupForm(ModelForm):
    class Meta:
        model = Group
        widgets = {
            'desc': Textarea({'rows': 5})
        }
        exclude = ('owner', 'members')


class GroupLogoForm(ModelForm):
    class Meta:
        model = Group
        fields = ('logo',)


class GroupCommentForm(ModelForm):
    class Meta:
        model = GroupComment


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = ('num_persons', 'average_price') # TODO 'photo'
        widgets = {
            'average_price': Select(attrs={'class': 'input-small'})
        }


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    file = forms.FileField()


class ImgTestForm(ModelForm):
    class Meta:
        model = ImageTest
        widgets = {
            'image': ImageCropWidget,
        }

#User related
class UploadAvatarForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'cropping')
        widgets = {
            'avatar': ImageCropWidget,
        }


class BasicProfileForm(ModelForm):
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) < 3:
            raise forms.ValidationError(u"请至少输入3个兴趣标签，这样会让别人更加了解你哦！")
        return tags


    class Meta:
        model = UserProfile
        fields = ('name', 'motto', 'birthday', 'gender', 'college', 'industry', 'work_for', 'occupation', 'tags')
        widgets = {
            'gender': RadioSelect(choices=GENDER_CHOICE, ),
            'birthday': SelectDateWidget(required=False, years=range(1916, 1996), attrs={'class': "input-small"}, )

        }


class BindProfileForm(ModelForm):
    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) < 3:
            raise forms.ValidationError(u"请至少输入3个兴趣标签吧，这样会让别人更加了解你哦！")
        return tags

    class Meta:
        model = UserProfile
        fields = ('name', 'gender', 'tags')
        widgets = {
            'gender': RadioSelect(choices=GENDER_CHOICE, ),
            #            'birthday' : SelectDateWidget(required=False, years=range(1916,1996), attrs={'class':"input-small"},)
        }


class PhotoForm(ModelForm):
    class Meta:
        model = UserPhoto
        fields = ('photo',)


#restaurant admin related
class OrderCheckInForm(forms.Form):
    code = forms.CharField(max_length=20, widget=(TextInput(attrs={'placeholder': "请输入用户就餐验证码"})))

