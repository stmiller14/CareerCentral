'''
update this template to set users password 
http://127.0.0.1:8000/accounts/reset/Ng/set-password/
'''
'''
#easy eay to check if email exists wit the User class
#User.objects.filter(email=email).exists():
print("users with thtat email "  ,my_form.get_users(email).__next__())



all_users=User.objects.all()
print(' all thje users ' , all_users)

'''



import json 
from .scrape.indeed_refactor import Indeed
from .scrape import multiprocess_simply, multithread_simply, async_monster, builder
from . import models
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from asyncio import run

@csrf_exempt
def reset_password(request):
    if request.method=='POST':
        my_form=PasswordResetForm(request.POST)
        if my_form.is_valid():
            email = my_form.cleaned_data["email"]
            if not  User.objects.filter(email=email).exists():
                return render(request, 'login.html' , {'error': 'email does not exist, please go to registration page'})
            my_form.save(subject_template_name='registration/password_subject.html',
            email_template_name='registration/password_reset_email.html', request=request)
            return redirect('/loginpage')
        else:
            return render(request, 'registration/password_reset_form.html', {'error':'Please Enter Valid Email'})
    return render(request, 'registration/password_reset_form.html'  )


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/loginpage')
def index(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage')
    if request.method=='POST':
        if 'rolename' not in request.POST.keys():
            models.save_search(request.user.email, json.loads(request.body))
            return HttpResponse('')
        resp=request.POST
        role, location =resp['rolename'] , resp['locationname']
        if 'indeed.x' in resp.keys():
            ret=list(Indeed().getrole(role, location).values())
        elif 'monster.x' in resp.keys():
            ret=run(async_monster.getrole_monster(role, location)).values()
        elif 'career.x' in resp.keys():
            ret=list( builder.getrole_career(role,location).values()  )
        elif 'glass.x' in resp.keys():
            ret=list(multiprocess_simply.getrole_simply(role,location).values())
            
        return render(request, 'index.html', {'results': ret}  )
    else:
        return render(request, 'index.html')



@csrf_exempt
def loginpage(request):
    logout(request)
    if request.method=='POST':
        resp=request.POST
        user_name, password=resp['user_name'] , resp['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect( '/', {'user_name': user_name}  )
        else:
            return render(request, 'login.html', {'error':'invalid login credentials' })
    return render(request, 'login.html' )

@csrf_exempt
def logoutuser(request):
    logout(request)
    return redirect('/loginpage' , {'error':None})




'''
need to get the saved jobs from DB and return in table format 
'''
@csrf_exempt
def saved_jobs(request):
    if not request.user.is_authenticated:
        return redirect('/loginpage')
    if request.method=='GET':
        results=models.fetch_saved_jobs(request.user.email)
        return render(request, 'saved_jobs.html', {'results': results})
    elif request.method=='POST':
        if 'redirect_home' in request.POST.keys():
            return redirect( '/', {'user_name': User.first_name}  )
        data= json.loads(request.body)
        models.delete_job(request.user.email, data)
        
    return render(request,'saved_jobs.html')

@csrf_exempt
def register_user(request):
    if request.method=='POST':
        resp=request.POST
        try:
            user = User.objects.create_user(resp['user_name'] , resp['email']  , resp['password'] )
            user.save()
            login(request, user)
            return redirect( '/', {'user_name': 'First time user: ' + str(request.user.first_name)}  )
        except IntegrityError:
            return False
         

@csrf_exempt
def save_job(request):
    pass
















#########################################




'''
def register(request):
    if request.method=='POST':
        resp=request.POST
        username, email, password=resp['username'] , resp['email'],  resp['password']
        if login.createuser(username, email, password):
            redirect('/')

'''


def returnyear(request, year, **kwargs):
    
    return HttpResponse(' in test year %s %s ' % (year, kwargs))

    '''
    return HttpResponse (
        json.dumps({ 
            'year': year, 
            'name': kwargs['name'] 
            }))
    '''
