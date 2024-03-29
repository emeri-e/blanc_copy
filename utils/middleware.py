from django.conf import settings
from django.utils.module_loading import import_string
from django.shortcuts import redirect
from django.contrib.auth import logout



class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.profile.active:
            logout(request)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response