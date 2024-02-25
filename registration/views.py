
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from . models import ProfileData
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from customization.models import Routine, Workout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
# Create your views here.


def change_credentials(request):
    if request.method == 'POST':
        username = request.POST.get('new_username')
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        if username:
            try:
                request.user.username = username
                request.user.save()
                messages.success(request, 'Username changed successfully.')
            except Exception as e:
                messages.error(request, f'Error changing username: {e}')
        
        if current_password and new_password1 and new_password1 == new_password2:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                # messages.success(request, 'Password changed successfully.')
                return redirect('/login')
            
            else:
                messages.error(request, 'Password change failed. Please check the form.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        elif not current_password:
            messages.error(request, 'Please provide your current password.')
      
    return render(request, 'change_credentials.html')



def home(request):
    page = 'dashboard'
    routines = Routine.objects.filter(user=request.user)
    if not routines.exists():
        routine = Routine.objects.create(user=request.user)
    else:
        routine = routines.first()
        
    workouts = routine.workout_set.all()
    try:
            profile_data = ProfileData.objects.get(user=request.user)
            height = profile_data.height / 100  # Convert height to meters
            weight = profile_data.weight
            gender = profile_data.gender
            avatar_url = profile_data.avatar.url
            bmi = weight / (height ** 2)
            bmi = round(bmi, 2)
            suggestion = get_bmi_suggestion(bmi, gender)  # Get BMI suggestion
    except ProfileData.DoesNotExist:
            # Handle case when profile data doesn't exist
            bmi = None
            suggestion = None
            gender = None
            avatar_url = None
    
    return render (request,'registration/home/dashboard.html',{'workouts':workouts,'page':page,'bmi': bmi, 'suggestion': suggestion,'sex' : gender,'avatar_url':avatar_url})

    



def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('mail')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            error_message = "Your password and confirm password are not the same!!"
            return render(request, 'registration/signup/index.html', {'error_message': error_message})
        else:
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                return redirect('login')
            except IntegrityError:
                error_message = "A user with this username or email already exists."
                return render(request, 'registration/signup/index.html', {'error_message2': error_message})
        
    return render(request, 'registration/signup/index.html')


def loginpage(request):
    error_message = None
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('password1')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            error_message = "Username or Password is incorrect!!!"
    
    return render(request, 'registration/login/index.html', {'error_message': error_message})

def profile(request):
    if request.method == 'POST':
        height = float(request.POST.get('height')) / 100  # Convert height to meters
        weight = float(request.POST.get('weight'))
        gender = request.POST.get('gender')
        
        bmi = weight / (height ** 2)
        bmi = round(bmi, 2)
        profile, created = ProfileData.objects.get_or_create(user=request.user)
        profile.height = height * 100  # Save height in cm
        profile.weight = weight
        profile.gender = gender
        
        
        profile.save()

        suggestion = get_bmi_suggestion(bmi, gender)  # Get BMI suggestion
         # Handle profile picture upload
         
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            myfolder='media'
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,myfolder))
            filename = fs.save(avatar.name, avatar)
            avatar_url = fs.url(filename)

            # Save the avatar URL to the user's profile or wherever you need
            profile.avatar = avatar_url
            profile.save()

        
        return render(request, 'registration/home/profile.html', {'bmi': bmi, 'suggestion': suggestion,'avatar_url': profile.avatar.url})
    else:
        try:
            profile_data = ProfileData.objects.get(user=request.user)
            height = profile_data.height / 100  # Convert height to meters
            weight = profile_data.weight
            gender = profile_data.gender
            avatar_url = profile_data.avatar.url
            bmi = weight / (height ** 2)
            bmi = round(bmi, 2)
            suggestion = get_bmi_suggestion(bmi, gender)  # Get BMI suggestion
            
        except ProfileData.DoesNotExist:
            # Handle case when profile data doesn't exist
            bmi = None
            suggestion = None
            gender = None
            avatar_url = None
            
        
        return render(request, 'registration/home/profile.html', {'bmi': bmi, 'suggestion': suggestion,'sex':gender,'avatar_url': avatar_url})

def get_bmi_suggestion(bmi, gender):
    if bmi is None:
        return "No BMI data available."
    elif bmi < 18.5:
        return 'You are underweight. Consider gaining some weight. Include nutrient-dense foods like nuts, seeds, and healthy fats in your diet. Start a strength training routine to build muscle mass.'
    elif 18.5 <= bmi < 24.9:
        return 'You have a healthy weight. Keep it up! Continue with a balanced diet and regular exercise routine.'
    elif 25 <= bmi < 29.9:
        if gender == 'male':
            return 'You are overweight. Consider losing some weight and focus on cardio exercises. Incorporate activities like running, cycling, or swimming into your routine.'
        else:
            return 'You are overweight. Consider losing some weight and focus on strength training exercises. Start with bodyweight exercises like squats, lunges, and push-ups.'
    elif 30 <= bmi < 34.9:
        if gender == 'male':
            return 'You are moderately obese. Focus on losing weight and consult a healthcare professional. Consider high-intensity interval training (HIIT) for better results. Incorporate more vegetables, lean proteins, and whole grains into your diet.'
        else:
            return 'You are moderately obese. Focus on losing weight and consult a healthcare professional. Consider combining cardio and strength training exercises. Incorporate more vegetables, lean proteins, and whole grains into your diet.'
    elif 35 <= bmi < 39.9:
        if gender == 'male':
            return 'You are severely obese. It is crucial to focus on losing weight under medical supervision. Consider a structured exercise program supervised by a fitness professional. Focus on portion control and avoiding processed foods.'
        else:
            return 'You are severely obese. It is crucial to focus on losing weight under medical supervision. Consider a structured exercise program supervised by a fitness professional. Focus on portion control and avoiding processed foods.'
    else:
        if gender == 'male':
            return 'You are morbidly obese. Immediate action is necessary for your health. Consult a healthcare professional for a personalized weight loss plan. Consider bariatric surgery as a last resort. Focus on portion control, regular exercise, and seeking support from a healthcare team.'
        else:
            return 'You are morbidly obese. Immediate action is necessary for your health. Consult a healthcare professional for a personalized weight loss plan. Consider bariatric surgery as a last resort. Focus on portion control, regular exercise, and seeking support from a healthcare team.'



def community(request):
    try:
            profile_data = ProfileData.objects.get(user=request.user)
            height = profile_data.height / 100  # Convert height to meters
            weight = profile_data.weight
            gender = profile_data.gender
            avatar_url = profile_data.avatar.url
            bmi = weight / (height ** 2)
            bmi = round(bmi, 2)
            suggestion = get_bmi_suggestion(bmi, gender)  # Get BMI suggestion
    except ProfileData.DoesNotExist:
            # Handle case when profile data doesn't exist
            bmi = None
            suggestion = None
            gender = None
            avatar_url = None
    return render(request,'registration/home/community.html',{'bmi': bmi, 'suggestion': suggestion,'sex':gender,'avatar_url':avatar_url})

def account(request):
    try:
            profile_data = ProfileData.objects.get(user=request.user)
            height = profile_data.height / 100  # Convert height to meters
            weight = profile_data.weight
            avatar_url = profile_data.avatar.url
            gender = profile_data.gender
            bmi = weight / (height ** 2)
            bmi = round(bmi, 2)
            suggestion = get_bmi_suggestion(bmi, gender)  # Get BMI suggestion
    except ProfileData.DoesNotExist:
            # Handle case when profile data doesn't exist
            bmi = None
            suggestion = None
            gender = None
            avatar_url = None
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        user = request.user
        
        # Check if the current password matches the user's password
        if check_password(current_password, user.password):
            # Check if the new passwords match
            if new_password1 == new_password2:
                # Set the new password for the user
                user.set_password(new_password1)
                user.save()
                # messages.success(request, 'Password changed successfully!')
                return redirect('/login')  # Redirect to the same page after password change
            else:
                messages.error(request, 'New passwords do not match!')
        else:
            messages.error(request, 'Current password is incorrect!')
    
    return render(request, 'registration/home/account.html',{'bmi': bmi, 'suggestion': suggestion,'sex':gender,'avatar_url':avatar_url})

def logout(request):
    try:
            profile_data = ProfileData.objects.get(user=request.user)
            height = profile_data.height / 100  # Convert height to meters
            weight = profile_data.weight
            avatar_url = profile_data.avatar.url
            gender = profile_data.gender
            bmi = weight / (height ** 2)
            bmi = round(bmi, 2)
            suggestion = get_bmi_suggestion(bmi, gender)  # Get BMI suggestion
    except ProfileData.DoesNotExist:
            # Handle case when profile data doesn't exist
            bmi = None
            suggestion = None
            gender = None
            avatar_url = None
    return render(request,'registration/home/logout.html',{'bmi': bmi, 'suggestion': suggestion,'sex':gender,'avatar_url':avatar_url})

def logoutconfimed(request):
    logout(request)
    return redirect('login')
    





