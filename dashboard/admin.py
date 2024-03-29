# admin.py
from django.contrib import admin
from .models import Address, BitgoWallet, Profile, Wallet, Bank_Account, Notification, Deposit, Withdrawal

class AddressInline(admin.TabularInline):
    model = Address

class BankAccountInline(admin.TabularInline):
    model = Bank_Account

class WalletInline(admin.TabularInline):
    model = Wallet

class NotificationInline(admin.TabularInline):
    model = Notification

class ProfileAdmin(admin.ModelAdmin):
    inlines = [WalletInline, BankAccountInline, NotificationInline, AddressInline]

class ProfileInline(admin.TabularInline):
    model = Profile

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'user')

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'acc_no', 'profile', 'bank', 'is_default']

class DepositAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'status', 'timestamp', 'amount', 'is_withdrawn', 'profile')
    list_filter = ('status', 'is_withdrawn')
    search_fields = ('transaction_id',)

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'amount', 'status', 'timestamp', 'bank_account')
    list_filter = ('status',)
    search_fields = ('id',)

admin.site.register(Address)
admin.site.register(BitgoWallet)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet)
admin.site.register(Bank_Account, BankAccountAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)

