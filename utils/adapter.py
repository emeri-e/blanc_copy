from django.utils.http import urlencode
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.urls import reverse
# from accounts.models import Referral,Profile
from dashboard.models import Wallet
from dashboard.profile_model import Profile
from django.contrib.auth import get_user_model

import logging
logger = logging.getLogger(__name__)




class OTPAdapter(DefaultAccountAdapter):

    def login(self, request, user):

        # Add GET parameters to the URL if they exist.

        super(OTPAdapter, self).login(request, user)

        # raise ImmediateHttpResponse(
        #     response=redirect(redirect_url)
        # )

        # Otherwise defer to the original allauth adapter.
        super(OTPAdapter, self).login(request, user)

    def save_user(self, request, user, form, commit=True):
        user = super(OTPAdapter,self).save_user(request, user, form, commit = True)
        

        # #check if user was used a referal link and create referral instance if true
        # if 'ref' in request.session:
        #     referral = request.session.get('ref')
        #     try:
        #         upline = get_user_model().objects.get(username = referral)
        #     except Exception as e:
        #         logger.exception('Couldnt link referral')
        #     else:
        #         Profile.objects.get_or_create(user = user)
        #         r= Referral.objects.create(
        #             upliner=upline.profile,
        #             downliner = user.profile
        #         )
        Profile.objects.get_or_create(user = user)

        
        # wallet = Wallet.objects.get_or_create(profile=profile)

        return user