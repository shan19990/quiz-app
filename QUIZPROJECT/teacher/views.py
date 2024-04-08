from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from .forms import TeacherLoginForm,TeacherRegisterForm

# Create your views here.
def TeacherLoginView(request):
    if request.method == "POST":
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user is not None and user.is_staff:
                login(request,user)
                print("Login success")
                return redirect("quiz-list")
            else:
                print("No user Present")

    form = TeacherLoginForm()
    return render(request, "teacher/teacher-portal-login.html",{"form":form})

def TeacherRegisterView(request):
    if request.method == "POST":
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.is_staff = True
            user.save()
            return redirect("student-login")
    else:
        form = TeacherRegisterForm()
    return render(request, "teacher/teacher-portal-register.html",{"form":form})