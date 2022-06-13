from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.admin import UserAdmin
from .models import Customuser, Driver, Head, Vehicle, Manager


# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {'fields': ('email', 'password','first_name','last_name','email','dob','profile_image','created_on' )}),
#         (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
#         (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
#         (_('Important dates'), {'fields': ('updated_on',)}),
#             # (_('user_info'), {'fields': ('first_name',)}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide', ),
#             'fields': ('email', 'password1', 'password2',),
#         }),
#     )
#     list_display = ['email', 'first_name', 'last_name', 'is_staff','is_manager','is_driver','is_head',]
#     search_fields = ('email', 'first_name', 'last_name',)
#     ordering = ('email', )

admin.site.register(Customuser)
admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(Manager)
admin.site.register(Head)
