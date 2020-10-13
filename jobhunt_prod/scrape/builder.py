"""
Career builder web crawl with thread design
"""
from requests import get 
from bs4 import BeautifulSoup
from threading import Thread
alldata={}
def get_career(url, role):
    titles=[]
    response = get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    href_container= soup.find_all('a', {'class': ['data-results-content block job-listing-item']})
    title_container= soup.find_all('div', {'class': ['col big col-mobile-inline']})
    career_site= "https://www.careerbuilder.com" 
    for  i, data in  enumerate(href_container):
        child_soup= BeautifulSoup(str(data), 'html.parser')
        title_container=child_soup.find('div' , {'class': ['data-results-title dark-blue-text b']})
        if title_container is not None:
            time_container=child_soup.find('div' , {'class': ['data-results-publish-time']})
            location_container=child_soup.find('div' , {'class': ['data-details']})
            href= career_site + data.attrs['href']
            ID= data.attrs['data-job-did']
            title=title_container.text
            all_data=location_container.text
            all_data=location_container.text.split('\n')
            company, location =all_data[1] , all_data[2]
            time= time_container.text 
            if role.upper() in title.upper():
                alldata[ID]=[ title, company, location, time , href]

def getrole_career(role, location):
    result={}
    if "," in location:
        location=location.split(',')
        if len(location)>=2:
            location=location[0].strip()+ "," + location[1].strip()
    url_first= 'https://www.careerbuilder.com/jobs?utf8=✓&keywords='+role+'&location='+location
    url= 'https://www.careerbuilder.com/jobs?utf8=✓&keywords='+role+'&location='+location+'&page_number='
    threads= [ Thread(target=get_career, args=( url +str(n) , role  ),daemon=True) for n in range(1, 30)]
    threads.append(Thread(target=get_career,  args=( url_first , role   ),daemon=True))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
   

    #cleaning the data
    for k, v in alldata.items():
        if v not in result.values():
            result[k]=v 
    alldata.clear()
    return result

#getrole_career('python', 'new york')