from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request ,*args, **kwargs):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        authenticated = request.user.is_authenticated
        url = request.path
        # if authenticated and url == settings.HOME_URL:
        #     messages.info(request, "Logged out automatically")
        #     logout(request)
        #
        # if not authenticated and url!= settings.HOME_URL and url!=settings.LOGIN_URL:
        #     messages.info(request, "Anonymous so stay in Home url")
        #     print("Not authenticated so stay at Home url")
        #     return redirect(settings.HOME_URL)


