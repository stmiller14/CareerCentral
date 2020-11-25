#linkedin
#    #url= "https://www.linkedin.com/jobs/search?keywords=Python&location=New%20York%2C%20New%20York%2C%20United%20States&geoId=102571732&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum="

'''
for i in  range(1,5):
    all_data=scrape( all_data , url+str(i) , ' new york')
'''



import requests
import urllib.request
import json
from bs4 import BeautifulSoup
from threading import Thread


def scrape( all_data , url, location):

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #content_container= soup.find_all('a', {'class': ["result-card__full-card-link"]})
    content_container= soup.find_all('li', {'class': [  "result-card job-result-card result-card--with-hover-state"]})

    for x, i in enumerate(content_container):
        try:
            title=i.a.span.text
            href=i.a['href']
            company=i.h4.a.text
            time=i.time.text
            all_data[href] =[title, company, time, href ]
        except AttributeError:
            pass
    return all_data



def start(role , location):
    all_data={}
    url= "https://www.linkedin.com/jobs/search?keywords="+ role + "&location=" + location+"&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum="
    threads= [ Thread(target=scrape, args=( all_data,  url +str(n) , role  ),daemon=True) for n in range(1, 10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return all_data



if __name__ == "__main__":
    ret= start('python' , 'new york')