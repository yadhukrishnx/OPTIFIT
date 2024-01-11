from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    context = {'active_button': 'home'}
    return render (request,'home.html',context)
# def landingpage(request):
#     return render (request,'landingpage.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            error_message = "Your password and confirm password are not the same!!"
            return render(request, 'signup.html', {'error_message': error_message})
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def ProfilePage(request):
    context = {'active_button': 'profile'}
    return render(request,'home+profile.html',context)
def CommunityPage(request):
    context = {'active_button': 'community'}
    return render(request,'home+community.html',context)
def AccountPage(request):
    context = {'active_button': 'account'}
    return render(request,'home+account.html',context)
def logout_confirmation(request):
    return render(request, 'home+logout.html')