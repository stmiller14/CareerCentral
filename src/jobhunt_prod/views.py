'''
refactor global var to a request.session[]=x to handle scaling http requests within heroku
login required decorator for searching
'''



import json 
from .scrape.indeed_refactor import Indeed
from .scrape import multiprocess_simply, multithread_simply, async_monster, builder, linkedin
from . import models
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm , UserCreationForm
from asyncio import run
from os import environ, getcwd
from django.contrib import messages
from . import custom_form 
import xlsxwriter
from io import BytesIO
from .api_generation import Generate_Token, Api_Response

@csrf_exempt
def reset_password(request):
    if request.method=='POST':
        '''
        sp=SpecialCharacterValidator(['a','b'])
        print('special validator')
        #print(sp.validate('Stephen'))
        print(sp.validate('stephenab'))
        '''
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

def change_password(request):
    return render(request, 'registration/password_reset_confirm.html'  )

def reset_done(request):
    return render(request, 'registration/password_reset_complete.html'  )

def get_api():
    API_KEY=""
    if not environ.get('IS_HEROKU', False):
        try: 
            from . import conf
            API_KEY=conf.API_KEY
        except ImportError:
            pass
    else:
        API_KEY = environ.get('API_KEY', None)
    return API_KEY

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/loginpage')
def index(request):
    ret={}
    API=get_api()
    if not request.user.is_authenticated:
        return redirect('/loginpage')
    if request.method=='POST':
        if 'rolename' not in request.POST.keys():
            models.save_search(request.user.email, json.loads(request.body))
            return HttpResponse('')
        resp=request.POST
        request.session['role'], request.session['location']=resp['rolename'] , resp['locationname']
        role, location =request.session['role'], request.session['location']
        print(' the request post' , request.POST.keys() ) ; 
        print(request.POST.get("optionsname"))
        jobengine=request.POST.get("optionsname")
        if jobengine:
            if 'Indeed' in jobengine:
                ret=Indeed().getrole(role, location)
            elif 'monster' in jobengine:
                ret=run(async_monster.getrole_monster(role, location))
            elif 'career' in jobengine:
                ret=builder.getrole_career(role,location) 
            elif 'glass' in jobengine:
                ret=multiprocess_simply.getrole_simply(role,location)
            elif 'link' in jobengine:
                ret=linkedin.start(role, location)
            request.session['hold_data']=ret
        request.session['site']=jobengine
        if'excel' in resp.keys():
            try:
                return excel_download(request, request.session['hold_data'],  API )
            except UnboundLocalError:
                return excel_download(request, {'error' :'error'} ,   API)
        if 'generate_key' in resp.keys():
            return generate_token(request,   API)
        return render(request, 'index.html', {'results': ret.values() ,  'API_KEY' : API}  )
    else:
        try:
            return render(request, 'index.html', {'results': request.session['hold_data'].values() , 'API_KEY' : API}  )
        except KeyError:
            return render(request, 'index.html', {'API_KEY' : API}  )

@csrf_exempt
def loginpage(request):
    request.session['hold_data']={}
    logout(request)
    if request.method=='POST':
        resp=request.POST
        user_name, password=resp['user_name'] , resp['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect( '/', {'user_name': request.user.first_name}  )
        else:
            return render(request, 'login.html', {'error':'invalid login credentials' })
    return render(request, 'login.html' )

@csrf_exempt
def logoutuser(request):
    request.session['hold_data']={}
    logout(request)
    return redirect('/loginpage' , {'error':None})

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
        models.delete_job(request.user.email, json.loads(request.body))
        
    return render(request,'saved_jobs.html')

@csrf_exempt
def register(request):
    if request.method=='POST':
        user_form=custom_form.UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            firstname = user_form.cleaned_data.get('first_name')
            email = user_form.cleaned_data.get('email')
            user_form.clean_email()
            user=user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect( '/', {'user_name': User.first_name}  )
        return render( request  ,'register_user.html', {'form': user_form})
    else:
        user_form = custom_form.UserForm()
    return render(request,'register_user.html', {'form': user_form})

@csrf_exempt
def save_job(request):
    pass

@csrf_exempt
def excel_download(request, ret ,  API):
    c=0
    output = BytesIO()
    workbook = xlsxwriter.Workbook( output)
    try:
        worksheet = workbook.add_worksheet(request.session['site'][:-1] ) 
        worksheet.write( 0 , 0 ,  'Role: ' + request.session['role']  + ' Location:' + request.session['location']   )
        for  v in ret.values():
            c+=1
            for x ,  data in enumerate(v):
                worksheet.write_column(c, x, [data])  
        workbook.close()
        output.seek(0)
    except KeyError:
        return render(request, 'index.html', {'results': ret.values() , 'API_KEY' : API}  )
    return HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@csrf_exempt
def generate_token(request, API):
    token=Generate_Token(request.user.email ).activate_key()
    return render(request, 'index.html', {'token': token, 'API_KEY' : API}  )













#########################################


def returnyear(request, year, **kwargs):
    
    #return HttpResponse(' in test year %s %s ' % (year, kwargs))
    return HttpResponse (
        json.dumps({ 
            'year': year, 
            'name': kwargs['name'] 
            }))
    
