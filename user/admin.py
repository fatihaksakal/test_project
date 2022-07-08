from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser, Employee, Customer


# Register your models here.


class MyUserAdmin(UserAdmin):
    model = NewUser

    fieldsets = (
        ('User info', {'fields': ('user_type', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio')}),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups',
            'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_type', 'email', 'first_name', 'last_name', 'password1', 'password2'), }),
    )

    list_display = ['id', 'email', 'user_type', 'first_name', 'last_name']
    list_display_links = ['id', 'email', 'first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['user_type', 'is_superuser', 'is_staff']
    actions = ["deactivate", "activate"]
    ordering = ['-id']

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

    def activate(self, request, queryset):
        queryset.update(is_active=True)


@admin.register(Employee)
class EmployeeUserAdmin(admin.ModelAdmin):
    employee_fieldsets = (
        ('Credentials', {'fields': ('uu_id',)}),
    )
    readonly_fields = ['uu_id']

    fieldsets = MyUserAdmin.fieldsets + employee_fieldsets


@admin.register(Customer)
class CustomerUserAdmin(MyUserAdmin, admin.ModelAdmin):
    customer_list_displays = ['company']
    customer_fieldsets = (
        ('XYZ Employee', {'fields': ('related_employee',)}),
        ('Company', {'fields': ('company',)}),
    )
    fieldsets = MyUserAdmin.fieldsets + customer_fieldsets
    list_display = MyUserAdmin.list_display + customer_list_displays


admin.site.register(NewUser, MyUserAdmin)
