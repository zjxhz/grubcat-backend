#coding=utf-8
from django import forms
from django.forms import ModelForm
from django.forms.widgets import *
from grubcat.eo.models import *


NUM_PERSON_CHOICE = [(x, "%s人" % x) for x in range(1,10)]

class OrderCreateForm(ModelForm):
    meal_id=forms.CharField(widget=HiddenInput)

    def clean(self):
        return super(OrderCreateForm,self).clean()
        #TODO check if the user can add the meal order; private/already have one

    class Meta:
        model = Order
        fields = ('num_persons',)
        widgets = {
            'num_persons': Select(choices=NUM_PERSON_CHOICE,),
            }

class DishForm(ModelForm):
    class Meta:
        model = Dish


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    file = forms.FileField()


class ImgTestForm(ModelForm):
    class Meta:
        model = ImageTest


class RestaurantCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    address = forms.CharField(max_length=256,
        help_text=u"No need to include city or district here"),
    tel = forms.CharField(max_length=20)
    tel2 = forms.CharField(max_length=20, required=False)
    introduction = forms.CharField(max_length=2000, widget=forms.Textarea)
    tags = forms.CharField(max_length=100,
        help_text=u"Separated by spaces, 5 tags at most ", #TODO validation
        required=False)
    business_districts = forms.ModelChoiceField(queryset=Region.objects.all(),
        empty_label=None)
    longitude = forms.FloatField()
    latitude = forms.FloatField()

    class Meta:
        model = Restaurant
        #fields = ("name", "address", )

    def save(self, commit=True):
        r = super(RestaurantCreationForm, self).save(commit=False)
        r.company_id = 1
        # r.tags

        
