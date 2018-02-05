from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Friend

def index(request):
    # print(User.objects.all())
    return render(request, 'friend2_app/index.html')

def register(request):
    # print request.POST
    response = User.objects.register(
        name = request.POST["name"],
        alias = request.POST["alias"],
        email = request.POST["email"],
        password = request.POST["password"],
        confirm_password = request.POST["confirm_password"],
        bday = request.POST["bday"],
    )
    
    if response['valid']:
        messages.add_message(request, messages.SUCCESS, 'Welcome to the site!')
        request.session["user_id"]=response["user"].id
        request.session["name"]=response["user"].name
        return redirect("/friends")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)
    return redirect("/")
 
def login(request):
    response = User.objects.login(
        email = request.POST["email"],
        password = request.POST["password"]
    )
    if response['valid']:
        messages.add_message(request, messages.SUCCESS, 'See you soon!')
        request.session["user_id"]=response["user"].id
        request.session["name"]=response["user"].name
        return redirect("/friends")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect("/")

def dashboard(request):
    person = User.objects.get(id=request.session['user_id'])
    users = User.objects.all()
    others = []
    for otheruser in users:
        if (otheruser.id != request.session['user_id']):
                others.append(otheruser)
    
    friends = Friend.objects.filter(friend1=person)
    friendship = []
    for friend in friends:
        friendship.append(friend.friend2)
    others2 = []
    for otheruser in others:
        if (otheruser not in friendship):
                others2.append(otheruser)
    
    context = {
        'person' : person,
        'users' : others2,
        'friends' : friendship
    }
    return render(request, 'friend2_app/dashboard.html', context)

def profile(request, id):
    show = User.objects.get(id=id)
    context = {
        'user' : show
    }
    return render(request, 'friend2_app/profile.html', context)

def addfriend(request, id):
    User.themanager.add(request.session['user_id'], id)
    return redirect('/friends')

def removefriend(request, id):
    User.themanager.remove(request.session['user_id'], id)
    return redirect('/friends')

def logout(request):
    request.session.clear()
    return redirect('/')