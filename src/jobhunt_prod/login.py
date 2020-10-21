'''
https://django-book.readthedocs.io/en/latest/chapter14.html#logging-in-and-out


#create a user 
#remove a user 
#authenticate the user
#login and save data into session to grab the user from any file
#log user out 

..hash the password before saving 
    Django hashes the password for you 
? where do these users get saved?>


'''


from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import redirect




def login():
    pass

def logout():
    pass


def is_authenticated():
    pass

def removeuser():
    pass





