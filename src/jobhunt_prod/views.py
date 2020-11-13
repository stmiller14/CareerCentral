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
hold_data={}
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
    global hold_data
    if not request.user.is_authenticated:
        return redirect('/loginpage')
    API=get_api()
    if request.method=='POST':
        if 'rolename' not in request.POST.keys():
            models.save_search(request.user.email, json.loads(request.body))
            return HttpResponse('')
        resp=request.POST
        request.session['role'], request.session['location']=resp['rolename'] , resp['locationname']
        role, location =request.session['role'], request.session['location']
        if 'indeed.x' in resp.keys():
            hold_data=ret=Indeed().getrole(role, location)
            request.session['site']=str(list(resp.keys())[-1])
        elif 'monster.x' in resp.keys():
            hold_data=ret=run(async_monster.getrole_monster(role, location))
            request.session['site']=str(list(resp.keys())[-1])
        elif 'career.x' in resp.keys():
            hold_data=ret=builder.getrole_career(role,location) 
            request.session['site']=str(list(resp.keys())[-1])
        elif 'glass.x' in resp.keys():
            hold_data=ret=multiprocess_simply.getrole_simply(role,location)
            request.session['site']=str(list(resp.keys())[-1])
        if'excel' in resp.keys():
            return excel_download(request, API )
        return render(request, 'index.html', {'results': ret.values() , 'API_KEY' : API}  )
    else:
        return render(request, 'index.html', {'results': hold_data.values() , 'API_KEY' : API}  )



@csrf_exempt
def loginpage(request):
    global hold_data
    hold_data.clear()
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
    global hold_data
    hold_data.clear()
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
def excel_download(request, API):
    global hold_data
    c=0
    output = BytesIO()
    workbook = xlsxwriter.Workbook( output)
    try:
        worksheet = workbook.add_worksheet(request.session['site'][:-1] ) 
        worksheet.write( 0 , 0 ,  'Role: ' + request.session['role']  + ' Location:' + request.session['location']   )
        for k , v in hold_data.items():
            c+=1
            for x ,  data in enumerate(v):
                worksheet.write_column(c, x, [data])  
        workbook.close()
        output.seek(0)
    except KeyError:
        return render(request, 'index.html', {'results': hold_data.values() , 'API_KEY' : API}  )
    return HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def generate_token(request):
    print('in generate API')
    return Generate_Token(request.user.email )












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
