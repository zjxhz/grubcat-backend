from ajax_select import LookupChannel
from django.db.models.query_utils import Q
from models import DishCategory

__author__ = 'qimeng'

class DishCategoryLookup(LookupChannel):

    model = DishCategory

    def get_query(self,q,request):
        result = DishCategory.objects.filter(name__icontains=q).order_by('name')
#        print result
#        if not result:
#            result = DishCategory.objects.create(name=q)
#            print result
        return result
#
#    def get_result(self,obj):
#        u""" result is the simple text that is the completion of what the person typed """
#        return obj.name
#
#    def format_match(self,obj):
#        """ (HTML) formatted item for display in the dropdown """
#        return self.format_item_display(obj)
#
#    def format_item_display(self,obj):
#        """ (HTML) formatted item for displaying item in the selected deck area """
#        return u"%s<div><i>%s</i></div>" % (escape(obj.name),escape(obj.email))