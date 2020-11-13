
'''

'''
from django.http import HttpResponse, StreamingHttpResponse

active_keys=set()


class Generate_API():
    '''
    return a web link that returns an HttpResponse JSON object
    serializable, bytesIO
    careerapp.API=key,role=?, location=?, engine=?.com
    Generate an API key.. one allowed per email at a time


    error messages to catch
    1. email is not registered
    2. user already has active key

    '''

    def __init__(self, engine , role , location): 
        self.engine=engine
        self.role=role
        self.location=location
        self.json_obj={}
        self.key=None
        self.errors={}
        

    def request(self, email ):
        '''
        get request from user. pass in email
        if valid email call response
        '''
        

    def activate_key(self):
        '''
        create a long key and store in valid key set
        '''
        pass

    def is_valid_key(self, key):
        is_valid=False
        if key in active_keys:
            is_valid=True
        return is_valid

    def response(self):
        if self.is_valid_key(self.activate_key()):
            try:
                '''
                query the system from the scrape scrips
                '''
                from views import hold_data
                self.json_obj=hold_data
                return HttpResponse(self.json_obj)
            except ImportError:
                self.errors[1]= 'ImportError'

            
        else:
            self.error_handler()


    def error_handler(self):
        return HttpResponse(self.errors)