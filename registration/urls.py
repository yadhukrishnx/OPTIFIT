from django.urls import path
from . import views

urlpatterns =[
    path("login/",views.loginpage,name='login'),
    path('',views.signup,name='signup'),
    path("signup/",views.signup,name='signup'),
    path("dashboard/",views.home,name='dashboard'),
    path("profile/",views.profile,name='profile'),
    path("community/",views.community,name='community'),
    path("account/",views.account,name='account'),
    path("logout/",views.logout,name='logout'),
    path('change-credentials/',views.change_credentials, name='change_credentials'),
    path("logoutconfirmed/",views.logoutconfimed,name='logoutconfirmed'),
    
]