from django.shortcuts import redirect
from django.urls import reverse

class CheckIfLoggedIn:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Continue with the request processing
        response = self.get_response(request)

        return response
