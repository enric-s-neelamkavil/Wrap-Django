from .views import signup,get_start,select_occupation,loader,signin,user_logout,dashboard
from django import contrib
from django.urls import include,path

urlpatterns = [
    path('',loader, name='loader'),
    path('get_start/',get_start,name='get_start'),
    path('select_occupation/',select_occupation,name='select_occupation'),
    path('signup/',signup, name='signup'),
    path('signin/',signin, name='signin'),
    path('user_logout/',user_logout, name='user_logout'),

    path('dashboard/',dashboard, name='dashboard'),

]