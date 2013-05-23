from fanju.models import User
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized

class UserObjectsOnlyAuthorization(Authorization):
    
    read_other = False
    def __init__(self, read_other=False):
        self.read_other = read_other
        
    def user_field(self, queryset):
        if hasattr(queryset.model, "user"):
            return "user"
        elif hasattr(queryset.model, "customer"):
            return "customer"
        elif hasattr(queryset.model, "from_person"):
            return "from_person"
    
    def is_user_object(self, object_list, bundle):    
        request_profile = bundle.request.user
        if isinstance(bundle.obj, User):
            bundle_user = bundle.obj
        else:
            bundle_user = getattr(bundle.obj, self.user_field(object_list))
        return bundle_user == request_profile

    def read_list(self, object_list, bundle):
        if self.read_other or isinstance(bundle.obj, User):
            return object_list
        
        user_field = self.user_field(object_list)
        request_profile = bundle.request.user
        f = {user_field:request_profile}
        return object_list.filter(**f)
    
    def read_detail(self, object_list, bundle):
        if self.read_other:
            return True
        return self.is_user_object(object_list, bundle)

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, not implemented")

    def create_detail(self, object_list, bundle):
        return self.is_user_object(object_list, bundle)

    def update_list(self, object_list, bundle):
        raise Unauthorized("Sorry, not implemented")

    def update_detail(self, object_list, bundle):
        return self.is_user_object(object_list, bundle)

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, not implemented.")

    def delete_detail(self, object_list, bundle):
        return self.is_user_object(object_list, bundle)
            