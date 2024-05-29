from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings

from dashboard.profile_model import Profile

# from dashboard.models import Wallet, Payment, Investment, Withdrawal
# from utils.models import History
# from accounts.models import Profile

ADMIN = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)

@receiver(post_save, sender = User)
def initialize_user(sender, instance, created, **kwargs):
    if created:
        # Wallet.objects.get_or_create(user = instance)
        Profile.objects.get_or_create(user=instance)

        # html = render_to_string('emails/admin-user-created.html', {'user': instance})
        # message = strip_tags(html)

        # try:
        #     send_mail(
        #         'New User Registered',
        #         message,
        #         settings.DEFAULT_FROM_EMAIL,
        #         [ADMIN,],
        #         html_message=html
        #     )
        # except:
        #     pass


# @receiver(post_save, sender=Payment)
# def initialize_payment(sender, instance, created, **kwargs):
#     if created:
#         history = History.objects.create(user=instance.user)
#         instance.history = history
#         instance.save()

#         html = render_to_string('emails/admin-payment-created.html', {'payment': instance})
#         message = strip_tags(html)
#         try:
#             send_mail(
#                 'New Payment Created',
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [ADMIN,],
#                 html_message=html
#             )
#         except:
#             pass



# @receiver(post_save, sender=Investment)
# def initialize_investment(sender, instance, created, **kwargs):
#     if created:
#         history = History.objects.create(user=instance.user)
#         instance.history = history
#         instance.save()

#         html = render_to_string('emails/admin-investment-created.html', {'investment': instance})
#         message = strip_tags(html)
#         try:
#             send_mail(
#                 'New Investment Created',
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [ADMIN,],
#                 html_message=html
#             )
#         except:
#             pass

# @receiver(post_save, sender=Withdrawal)
# def initialize_withdrawal(sender, instance, created, **kwargs):
#     if created:
#         history = History.objects.create(user=instance.user, withdrawal=instance)
#         instance.history = history
#         instance.save()

#         html = render_to_string('emails/admin-withdrawal-created.html', {'withdrawal': instance})
#         message = strip_tags(html)
#         try:
#             send_mail(
#                 'New Withdrawal Created',
#                 message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [ADMIN,],
#                 html_message=html
#             )
#         except Exception as e:
#             print(e)