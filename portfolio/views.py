from django.shortcuts import render , redirect
from django.http import HttpResponse  
from django.contrib.auth import authenticate , login as auth_login
from django.contrib.auth.models import User 

def index(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Hello,{request.user.username}.")
    
    return HttpResponse("Hello, world. You're at the portfolio index.") 

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, "login.html", {"error_message": "Invalid credentials"})
        auth_login(request, user)
        return redirect("index")
    else:
       
        return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname  = request.POST.get("lastname")
        username  = request.POST.get("username")
        email     = request.POST.get("email")
        password  = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error_message": "Username already exists"})
        
        user = User.objects.create_user(username=username, password=password, email=email,
                                        first_name=firstname, last_name=lastname)
        auth_login(request, user)
        return redirect("index")
    else:
        return render(request, "signup.html")