from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from chatbot_tutorial.forms import SignupForm
from django.contrib import messages

from chatbot_tutorial.models import User, ButtonHistory


def chat(request, user_id):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] != data['confirm_password']:
                return HttpResponse("Password and confirm password mismatches.")
            user = form.save()
            user.set_password(data['password'])
            user.save()
            html = "Signup success. Please <a href=\"/login/\">Login</a> to continue."
            return HttpResponse(html)
        else:
            return HttpResponse("Form error: " + str(form.errors))
    form = SignupForm()
    return render(request, 'chatbot_tutorial/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                user_id = user.id
                return HttpResponseRedirect(f"/chat/{str(user_id)}/")
            else:
                return HttpResponse("Invalid credentials. Please try to <a href=\"/login/\">Login</a> with correct credentials.")
        else:
            return HttpResponse("Form error: " + str(form.errors))
    form = AuthenticationForm()
    return render(request, 'chatbot_tutorial/login.html', {'form': form})


def users_list(request):
    users = User.objects.all().exclude(is_superuser=True)
    return render(request, 'chatbot_tutorial/users.html', {'users': users})


def respond_to_websockets(message):
    user_id = message.get('user_id')
    button_history = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)

            if not user.button_history:
                new_button = ButtonHistory.objects.create(fat=0, stupid=0, dumb=0)
                user.button_history = new_button
                user.save()
            button_history = user.button_history

        except Exception as e:
            print(e)
            pass
    jokes = {
     'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
     'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
     'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""] 
     }  

    result_message = {
        'type': 'text'
    }
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])
        if button_history:
            button_history.fat += 1
            button_history.save()
    
    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])
        if button_history:
            button_history.stupid += 1
            button_history.save()
    
    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])
        if button_history:
            button_history.dumb += 1
            button_history.save()

    elif message['text'] in ['hi', 'hey', 'hello']:
        result_message['text'] = "Hello to you too! If you're interested in yo mama jokes, just tell me fat, stupid or dumb and i'll tell you an appropriate joke."
    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    return result_message
    
