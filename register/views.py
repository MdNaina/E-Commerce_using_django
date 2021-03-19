from django.shortcuts import render, redirect
from django.http import JsonResponse
from .form import RegisterForm
from .otp import sendOtp
from random import randrange
from django.contrib.auth.models import User
import json


def otpgerate():
    out = ''
    for i in range(1,6):
        out += str(randrange(0,9))
    return out

opt2 = otpgerate()

#otp page
def otp(request):
    if request.method == 'POST':
        print(opt2)
        temp = json.loads(request.COOKIES['temp'])
        email = temp['email']
        print('email: ',email)
        otp = request.POST['otp']
        
        if otp == opt2:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            print('account is created successfully')
            return redirect('/')
        else:
            print('opt is not match')
    else:
        return render(request,'otp.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            print('password is not match')
            return redirect('/register/')
        elif User.objects.filter(username=username).exists():
            print('username is already exist')
            return redirect('/register/')
        elif User.objects.filter(email=email).exists():
            print('email is already exist')
            return redirect('/register/')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.is_active = False
            user.save()
            
            print(opt2)
            sendOtp(request=request,email=email,value=opt2)          
        return redirect('/otp/')
    else:
        return render(request, 'register.html')