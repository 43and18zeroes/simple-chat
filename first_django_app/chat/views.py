from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Chat, Message
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    """
    This is a view to render the chat html.
    """
    if request.method == "POST":
        print("Received data " + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(
            text=request.POST["textmessage"],
            chat=myChat,
            author=request.user,
            receiver=request.user,
        )
        serialized_obj = serializers.serialize('json', [ new_message ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    lastMessage = chatMessages.last()
    return render(request, "chat/index.html", {"messages": chatMessages, "last_message": lastMessage})


def login_view(request):
    redirect = request.GET.get("next")
    if request.method == "POST":
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get("redirect"))
        else:
            return render(
                request,
                "auth/login.html",
                {"wrongPassword": True, "redirect": redirect},
            )
    return render(request, "auth/login.html", {"redirect": redirect})


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("reg_username")
        password = request.POST.get("reg_password")

        if not username:
            messages.error(request, "The username field is required.")
            return render(request, "auth/register.html")

        if not password:
            messages.error(request, "The password field is required.")
            return render(request, "auth/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, "auth/register.html")

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful. You can now log in.")
        print(user)
        # return HttpResponseRedirect("/login/")

    return render(request, "auth/register.html")
