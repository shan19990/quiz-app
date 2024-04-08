from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from .forms import StudentLoginForm,StudentRegisterForm

# Create your views here.
def StudentLoginView(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user is not None and not user.is_staff:
                login(request,user)
                print("Login success")
                return redirect("quiz-list")
            else:
                print("No user Present")

    form = StudentLoginForm()
    return render(request, "student/student-portal-login.html",{"form":form})

def StudentRegisterView(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            return redirect("student-login")
    else:
        form = StudentRegisterForm()
    return render(request, "student/student-portal-register.html",{"form":form})

def StudentLogoutView(request):
    logout(request)
    return redirect("student-login")