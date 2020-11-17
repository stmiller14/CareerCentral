
'''
careercentral.herokuapp.com/API=123,role=python, location=New York
'''
from django.http import HttpResponse, StreamingHttpResponse
import json 
from .scrape.indeed_refactor import Indeed
from .scrape import multiprocess_simply, multithread_simply, async_monster, builder
from django.contrib.auth.models import User
import secrets

active_keys={'stephendmiller14@gmail.com' : '123'}


class Generate_Token():

    def __init__(self, email): 
        self.key=None
        self.email=email
        self.errors={}
        
    def activate_key(self):
        token=secrets.token_urlsafe(10)
        active_keys[self.email]=token
        print('token is ' , token , self.email)
        print('all keys ', active_keys)
        return token

    def is_valid_key(self, key):
        is_valid=False
        if key in active_keys.values():
            is_valid=True
        return is_valid

    def getkey(self, email) :
        return active_keys[self.email]

    def error_handler(self):
        self.errors={"1" : "error"}
        return HttpResponse(self.errors)


class Api_Response():

    def response(self, token, role , location):
        self.errors={'error':'errors'}
        if str(token) in active_keys.values():
            ret=Indeed().getrole(role, location)
            return HttpResponse (
                json.dumps({ 
                    'Role': role, 
                    'Location': location, 
                    'Jobs': ret
                    }  , indent=4))

        else:
            return HttpResponse( json.dumps(
                    {'error':'invalid key '}
                    ))

    def error_handler(self):
        self.errors={"1" : "error"}
        return HttpResponse(self.errors)