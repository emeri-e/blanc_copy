from django.contrib import admin
from core_app_root.user_services.bankmanagement.models import UserBankAccountDetails,BankAdminManager
# Register your models here.
admin.site.register(UserBankAccountDetails)
from django.contrib import admin
from .models import BankAdminManager

from django.contrib import admin
from .models import BankAdminManager

class BankAdminManagerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(BankAdminManager, BankAdminManagerAdmin)

