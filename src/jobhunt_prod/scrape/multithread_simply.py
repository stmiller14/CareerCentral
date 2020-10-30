"""
simply hired using threading 

"""

import requests
import urllib.request
import json
from bs4 import BeautifulSoup
from threading import Thread

import os
import psutil

alldata={}
def get_simply(url, role):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    content_container= soup.find_all('div', {'class': ['SerpJob-jobCard']})
    link= 'https://www.simplyhired.com'
    for content in content_container:
        title=content.h2.text
        href=None
        try:
            href=content.h2.a['href']
        except TypeError:
            print ("no href found")
        
        company=content.h3.text
        summary=content.p.text
        if title is not None and role.upper() in title.upper():
            if href is not None:
                href=link+href
                alldata[href]=[title, company, summary, href]
        
        
        
      
      
## scrape through 11 pages of simply using a thread for each I/O (4x faster)
def getrole_simply(role, location):
    global alldata
    result,threads={},[]
    if "," in location:
        location=location.split(',')
        location= location[0].strip()+ "," + location[1].strip()
    url_first= 'https://www.simplyhired.com/search?q='+role+'&l='+location
    url= 'https://www.simplyhired.com/search?q='+role+'&l='+location + '&pn='
    #processor_count= multiprocessing.cpu_count()
    threads= [ Thread(target=get_simply, args=( url +str(n)  , role  ),daemon=True) for n in range(1, 1)]
    threads.append(Thread(target=get_simply,  args=( url_first ,  role    ),daemon=True))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    #clean the data
    for k, v in alldata.items():
        if v not in result.values():
            result[k]=v 
    alldata.clear()
    return result

if __name__ == "__main__":
    getrole_simply('python', 'new york')
    process = psutil.Process(os.getpid())
    print('total memory usage: ' , process.memory_info().rss , psutil.cpu_percent())  # in bytes 