from rest_framework import permissions

########### Personalisation des permissions des utilisateurs #########

class IsStaffUserPermission(permissions.DjangoModelPermissions):
    
    # dict variable of permissions to be allowed to user depending of the http method
    perms_map = { # copy from the permissions.DjangoModelPermissions and personalize
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
    
    
            # how to add new conditions to match by a how before assign his permissions
            
    # def has_permission(self, request, view):
    #     # can add all condition to be matched by a user before assign it any permissions 
    #     # for example if the user.get_username == 'kalmogo' return True and ...
        
    #     user = request.user
    #     return super().has_permission(request, view) if user.is_staff else False
    
    
        # understanding how permission works
        
    # def has_permission(self, request, view):
    #     user = request.user

    #     # discovery of same methods and attributs related to a django.contib.auth.User instance
    #     print(user.get_all_permissions())
    #     print(user.get_group_permissions())
    #     print(user.get_username())
    #     print(user.last_login)
    #     print(user.is_active)

    #     if user.is_staff:
    #         # permission format description: "appname.verbs_modelname"
    #         if user.has_perms("todos.add_quotation"): 
    #             return True
    #         if user.has_perms("todos.delete_quotation"):
    #             return True
    #         if user.has_perms("todos.view_quotation"):
    #             return True
    #         return bool(user.has_perms("todos.change_quotation"))
        
    #     return False