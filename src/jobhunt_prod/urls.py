"""


accounts/auth.urls included for the password reset feature:
    accounts/login/ [name='login']
    accounts/logout/ [name='logout']
    accounts/password_change/ [name='password_change']
    accounts/password_change/done/ [name='password_change_done']
    accounts/password_reset/ [name='password_reset']
    accounts/password_reset/done/ [name='password_reset_done']
    accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    accounts/reset/done/ [name='password_reset_complete']

anaconda3/lib/python3.7/site-packages/django/contrib/auth
"""
from django.contrib import admin
from django.urls import path , include
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>', views.returnyear , kwargs= { 'name' : 'SM'} , name="returnyear"  ), 
    path('admin/', admin.site.urls),
    path('loginpage', views.loginpage, name='loginpage'),
    path('logout', views.logoutuser, name='logoutuser'),
    path('saved_jobs', views.saved_jobs, name="saved_jobs"),
    path('', views.save_job, name="save_job"),
    path('accounts/password_reset/',views.reset_password,name="password_reset"),
    path('accounts/login/',views.loginpage,name="loginpage"),
    path('accounts/', include('django.contrib.auth.urls')), # new
    
]
