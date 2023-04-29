from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as authlogin,logout
from myapp.forms import NewuserForm
from django.contrib import messages
import pyrebase
# import json
from django.shortcuts import redirect

config = {
  "apiKey": "AIzaSyAYdE1pdvYX9BYb0phiTPoVnbSnqaqIA20",
  "authDomain": "cloud-based-smart-power-supply.firebaseapp.com",
  "databaseURL": "https://cloud-based-smart-power-supply-default-rtdb.firebaseio.com/",
  "projectId": "cloud-based-smart-power-supply",
  "storageBucket": "cloud-based-smart-power-supply.appspot.com",
  "messagingSenderId": "629141012859",
  "appId": "1:629141012859:web:332c9b80c64aa0a2ecbdde"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def home(request):
    if request.user.is_authenticated:
        print('Authenticated user')

        input_voltage = database.child("Servo").child("INPUT VOLTS").get().val()
        output_voltage = database.child("Servo").child("OUTPUT VOLTS").get().val()
        data = {
            "input_voltage": input_voltage,
            "output_voltage":output_voltage,
        }
        
        return render(request, 'main/home.html',data)

    else:
        return redirect("login")


def registerUser(request):
    form = NewuserForm()

    if request.method == 'POST':
        form = NewuserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registratioin Succesfull')
        
        else:
            messages.error(request,'Registration UnSuccesfull -- Invalid Inputs')
            print("Unseccesfull")


    context = {
        'form':form,
    }    
    return render(request, 'main/register.html',context)
    
    
def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                authlogin(request, user)
                messages.success(request,"You are sucessfully Logged In")
                # return render('main/home.html')
                return redirect('home')
                
            else:
                messages.error(request,"Invalid Credentials")
        else:
            messages.error(request,"Invalid Credentials")

    form = AuthenticationForm()
    context = {
        'form':form,
    }
    
    return render(request, 'main/login.html', context )


def user_logout(request):
    logout(request)
    return redirect('login')