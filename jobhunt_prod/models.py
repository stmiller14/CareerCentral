from django.db import models, connection
#DB processing here 



def connect():
    with connection.cursor() as cursor:
        cursor.execute('''select email from public."user"''' )
        #row = cursor.fetchall()
        row=cursor.fetchone()
        print('row data ', row )
        return row


