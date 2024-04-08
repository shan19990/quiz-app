from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

class FormSubmissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.session.get('form_submitted') and request.path == '/question_add/': 
            del request.session['form_submitted']
            return redirect('student-login')
        
        return response