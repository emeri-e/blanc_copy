from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from bitgo.bitgo_base import BitGo
from bitgo.functions import fetch_deposits, update_comment
from bitgo.models import Address, Transaction

# from core_app_root.security.user.models import User
from decimal import Decimal as D
import uuid
from django.core.validators import MinValueValidator

from dashboard.profile_model import Profile
from management.models import BitgoWallet



    
class Wallet(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='wallet')
    available = models.DecimalField(max_digits = 12, decimal_places = 2, default = D(0.00), validators=[MinValueValidator(0)])
    # usdt = models.DecimalField(max_digits = 12, decimal_places = 2, default = D(0.00))
    
    # @property
    # def total_referral(self):
    #     downlines = self.profile.downlines.all()
    #     total = sum([float(downline.upline_reward) for downline in downlines if downline.completed])
    #     return total
    
    @property
    def usdt_balance(self):
        pass

    def __str__(self) -> str:
        return f'wallet of {self.profile.user.get_username()}'

    def _credit(self, amount: float):
        self.available += amount

    def _debit(self, amount: float):
        self.available -= amount


class Bank_Account(models.Model):
    class Banks(models.TextChoices):
        ACCESS_BANK = '044', 'Access Bank'
        GT_BANK = '058', 'GTBank'

    name = models.CharField(max_length=50)
    acc_no = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='bank_accounts')
    bank = models.CharField(choices=Banks.choices, max_length=3, default=Banks.ACCESS_BANK)  
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @property
    def bank_name(self):
        return dict(self.Banks.choices)[self.bank]
    

    
class Notification(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    read = models.BooleanField(default=False)

    @classmethod
    def from_txn(cls, txn):
        cls.objects.create(subject=f'{txn.__name__} {txn.status}', message=f'your {txn.__name__} for {txn.amount} has {txn.status}', user= txn.user)

    
# class History(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='history')
#     logs = ArrayField(
#         models.CharField(max_length=50),
#         default=list
#     )

#     def log(self, message):
#         msg = str(timezone.datetime.now()) + f'::{message}'
#         self.logs.append(msg)
#         self.save()

#     def get_logs(self):
#         logs = []
#         for item in self.logs:
#             date, message = item.split('::')
#             d = timezone.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
#             logs.append((d, message))
#         return logs

#     @classmethod
#     def history(cls, user):
#         all_history = []
#         if user == 'all':
#             histories = cls.objects.all().order_by('-id')
#         else:
#             histories = cls.objects.filter(user = user).order_by('-id')

#         for obj in histories:
#             if hasattr(obj, 'payment'):
#                 all_history.append(obj.payment)
#             elif hasattr(obj, 'investment'):
#                 all_history.append(obj.investment)
#             elif hasattr(obj, 'withdrawal'):
#                 all_history.append(obj.withdrawal)

#         # all_history.reverse()
#         return all_history


class Deposit( models.Model):
   
    class Status(models.TextChoices):
        PENDING = 'pending','pending'
        CANCELLED = 'canceled','canceled'
        COMPLETE = 'complete','complete'
        FAILED = 'failed', 'failed'
        
    
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    status = models.CharField(max_length = 20, choices = Status.choices, default = Status.PENDING)
    timestamp = models.DateTimeField(auto_now_add = True)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name="deposits")
    is_withdrawn = models.BooleanField(default=False)  # True if withdrawn, False otherwise
    address = models.ForeignKey(Address, on_delete= models.CASCADE, related_name='transactions')
    
    def __str__(self):
        return self.transaction_id
    
    
    class Meta:
        ordering = ['-timestamp',]

    def __str__(self):
        return self.user.username + '-' + str(self.id)[:3]

    def failed(self):
        if self.status == self.Status.FAILED:
            return True
        return False

    def update_at_bitgo(self):
        update_comment(self) #update at bitgo functions


    def confirm_deposit(self):
        '''Confirms that the users payment have been recieved by the platform'''
        
        self.update_at_bitgo()

        with transaction.atomic():
            self.status = Deposit.Status.COMPLETE
            self.is_withdrawn = True
            wallet = self.user.wallet
            wallet._credit(self.amount)
            self.save()
            wallet.save()

            Notification.from_txn(self)

            
    def decline_deposit(self): 
        self.status = Deposit.Status.FAILED
        self.save()
        Notification.from_txn(self)

    @classmethod
    def update_deposits(cls, profile):
        addresses = profile.addresses
        if addresses < BitgoWallet.objects.count():
            Address.initialise_addresses(profile)
            return
        
        deposits_data = fetch_deposits()

        for dep in deposits_data: 
            deposit, created = cls.objects.get_or_create(id=dep['transaction_id'], defaults=dep)

            if created:
                if dep['comment'] != 'withdrawn':
                    deposit.confirm_deposit()
                


class Withdrawal(models.Model):


    class Status(models.TextChoices):
        COMPLETE = 'complete', 'COMPLETE'
        PENDING = 'pending', 'PENDING'
        FAILED = 'failed', 'FAILED'

        __empty__ ='PENDING'


    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE, related_name="withdrawals")
    amount = models.DecimalField(max_digits = 12, decimal_places = 2, default = D(0.00))
    status = models.CharField(max_length=20 ,choices = Status.choices, default = Status.PENDING)
    timestamp = models.DateTimeField(auto_now_add = True)
    bank_account = models.ForeignKey(Bank_Account,on_delete = models.CASCADE, related_name="withdrawals", null=True)

    class Meta:
        ordering = ('-timestamp', '-id')

    def __str__(self):
        return self.user.username + str(self.id)[:3]

    @property
    def pending(self):
        return self.status == self.Status.PENDING

    def confirm(self):
        with transaction.atomic():
            self.status = Withdrawal.Status.COMPLETE        
            wallet = self.user.wallet
            wallet._debit(self.amount)
            self.save()
            wallet.save()

            Notification.from_txn(self)

    def decline(self):
        self.status = Withdrawal.Status.FAILED
        Notification.from_txn(self)


