from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.


class RegisterAPIView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration.html", context=context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=name, password=password)
            login(request, user)
            return redirect("../")
        else:
            print("Всё хуйня давай по новой")
            print(form.errors)
            form = UserCreationForm()
        return render(request, "registration.html", context={"form": form})


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        logout(request)
        messages.success(request, ("Вы вышли из аккаунта"))
        return redirect("/")


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        messages.success(request, ("Некорректно введены данные"))
        return render(request, "login.html")

def register_user_render(request):
    return render(request, "registration.html")

