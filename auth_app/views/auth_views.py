from django.shortcuts import render, redirect
from auth_app.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

# Create your views here.


@csrf_exempt
def login_user(request):
    if request.method == "GET":
        return render(request, "auth_app/login.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if len(username) == 0 or len(password) == 0:
            messages.add_message(request, messages.INFO, "write correctly")
            return redirect("/login")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("/")

        return redirect("/user/login")


@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


@csrf_exempt
def register_user(request):
    if request.method == "GET":
        return render(request, "auth_app/register_user.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST.get("confirm_password")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        user_type = request.POST.get("user_type")

        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            messages.add_message(request, messages.INFO, "username exist")
            return redirect("/user/register/")

        if len(username) <= 0:
            messages.add_message(
                request, messages.INFO, "username's length is too short"
            )
            return redirect("/user/register/")

        if password != confirm_password:
            messages.add_message(request, messages.INFO, "confirm password")
            return redirect("/user/register/")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    phone_number=phone_number,
                    email=email,
                    user_type=user_type,
                )
        except Exception:
            return redirect("/")

        return redirect("/user/login")
