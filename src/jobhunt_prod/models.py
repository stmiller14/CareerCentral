from django.db import models, connection
from datetime import datetime
#DB processing here 



def initialize_connection():
    return connection.cursor()

def save_search( email, data):
        cursor=initialize_connection()
        MAX_NUM=8
        link=""
        for key, value in data.items():
            row_data=[email, datetime.now()]
            for  col in value:
                if 'http' in col:
                    link=col
                else:
                    row_data.append(col)
            counter=MAX_NUM - len(value)
            while  counter>0:
                row_data.append('')
                counter -=1
            row_data.append(link)
            save_search_query = """INSERT INTO public."jobs" (email ,  datetime , role , description , location,  company , link, junk , junk2, junk3) VALUES (%s,%s,%s, %s, %s,%s,%s, %s,%s ,%s)""" 
            cursor.execute(save_search_query, tuple(row_data))
            connection.commit()

def fetch_saved_jobs(email):
    cursor=initialize_connection()
    cursor.execute('''select  distinct  role , description , location,  company , link, junk , junk2, junk3 from public."jobs" where email = %s''', (email, ))
    return list(cursor.fetchall()) 

def delete_job( email , data):
    cursor=initialize_connection()
    cursor.execute(""" delete from public."jobs"  where email  =  %s and junk3 = %s""" , (email, data[1] ))
    connection.commit()