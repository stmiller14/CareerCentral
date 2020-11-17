
'''
careercentral.herokuapp.com/API=123,role=python, location=New York
'''
from django.http import HttpResponse, StreamingHttpResponse
import json 
from .scrape.indeed_refactor import Indeed
from .scrape import multiprocess_simply, multithread_simply, async_monster, builder
from django.contrib.auth.models import User
import secrets



class Generate_Token():
    active_keys={'stephendmiller14@gmail.com' : '123'}

    def __init__(self, email): 
        self.key=None
        self.email=email
        self.errors={}
    
    def activate_key(self):
        token=secrets.token_urlsafe(10)
        self.addtoactive(self.email, token)
        return token

    def is_valid_key(self, key):
        is_valid=False
        if key in self.getallkeys():
            is_valid=True
        return is_valid


    @classmethod
    def addtoactive(cls, email, token):
        cls.active_keys[email]=token
        print('all keys ', cls.active_keys)
    @classmethod
    def getallkeys(cls):
        return cls.active_keys
    
    def error_handler(self):
        self.errors={"1" : "error"}
        return HttpResponse(self.errors)

class Api_Response():
    def response(self, token, role , location):
        active_keys=Generate_Token('api').getallkeys()
        self.errors={'error':'errors'}
        print('the active keys are ' ,  active_keys)
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