"""
simply hired using multi process design

"""

from requests import get
from bs4 import BeautifulSoup
from threading import Thread
import multiprocessing
from os import getpid
import psutil



def get_simply(url, role ):
    alldata={}
    response = get(url, headers={'User-Agent': 'Mozilla/5.0'})
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
    return alldata 
        
      
## scrape through 11 pages of simply using a multi processing for each I/O (4x faster)
def getrole_simply(role, location):
    test_data ={} 
    if "," in location:
        location=location.split(',')
        location= location[0].strip()+ "," + location[1].strip()
    url_first= 'https://www.simplyhired.com/search?q='+role+'&l='+location
    url= 'https://www.simplyhired.com/search?q='+role+'&l='+location + '&pn='
    #processor_count= multiprocessing.cpu_count()
    pool=multiprocessing.Pool(11)
    iterable = zip( [ url +str(i)  if i != 0 else  url_first  for i in range(1,30)   ],  [role for i in range(1,30)  ] )
    result_pool=pool.starmap( get_simply, iterable) 
    pool.close() 
    pool.join()
    
    
    for i, p in enumerate(result_pool):
        for key, value in p.items():
            if value not in test_data.values():
                test_data[key]= value 
    return test_data

process = psutil.Process(getpid())
print('total memory usage: ' , process.memory_info().rss , psutil.cpu_percent())  # in bytes 