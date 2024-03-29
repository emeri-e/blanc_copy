from django.db import models
from core_app_root.security.user.models import User
# Create your models here.
class UserBankAccountDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bank_code=models.CharField(max_length=2000,null=True,blank=True)
    account_number=models.CharField(max_length=2000,unique=True)
    account_name=models.CharField(max_length=2000,null=True,blank=True)
    bank_name=models.CharField(max_length=2000,null=True,blank=True)
    
class BankAdminManager(models.Model):
    bank_code=models.CharField(max_length=1000,null=True,blank=True)
    bank_name=models.CharField(max_length=5000,null=True,blank=True)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"{self.admin_user} added a new bank details with bank name {self.bank_name} and bank code {self.bank_code}"