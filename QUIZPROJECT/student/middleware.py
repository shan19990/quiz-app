from django.shortcuts import redirect
from django.urls import reverse

class CheckIfLoggedIn:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and \
           request.path != reverse('student-login') and \
           not request.path.startswith('/admin/') and \
           not request.path.startswith('/register/') and \
           not request.path.startswith('/teacher/'):
            return redirect('student-login')

        # Continue with the request processing
        response = self.get_response(request)

        return response
