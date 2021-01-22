'''
Indeed scrape with multi thread design
no need for class but whatever..coulda just used func design

need to connect to public proxies 
'''


import requests
from bs4 import BeautifulSoup
from threading import Thread
import random
all_data={}
i=0
class Indeed():
    def __init__(self):
        self.desc={}


    def get_indeed(self,  url, role ,proxies, allproxies, x=0 ):
        global i
        global all_data
        header_link='https://www.indeed.com'
        x+=1
        entire_container=None
        try:
            response = requests.get(url, proxies=proxies ,  headers={'User-Agent': 'Mozilla/5.0'} , timeout= 5)
            soup = BeautifulSoup(response.text, 'html.parser')
            entire_container= soup.find_all  ('div' ,  {'class' : ['jobsearch-SerpJobCard unifiedRow row result' ] })
        
        except requests.exceptions.ProxyError:
            if x<=3:
                self.get_indeed(  url, role ,self.get_session(allproxies), allproxies , x )
            else:
                return
        except requests.exceptions.ConnectTimeout:
            if x<=3:
                self.get_indeed(  url, role ,self.get_session(allproxies), allproxies , x )
            else:
                return
        except requests.exceptions.ConnectionError:
            if x<=3:
                self.get_indeed(  url, role ,self.get_session(allproxies), allproxies , x )
            else:
                return
        except requests.exceptions.ReadTimeout:
            if x<=3:
                self.get_indeed(  url, role ,self.get_session(allproxies), allproxies , x )
            else:
                return

        if not entire_container:
            return

        for  data  in entire_container:
            ID= data.attrs['id']
            child_soup=BeautifulSoup(str(data), 'html.parser')
            title_container=child_soup.find('h2' , {'class': ['title']}) 
            title=title_container.a.attrs['title']
            href= header_link + str(title_container.a.attrs['href'])
            location_container=child_soup.find('div' , {'class': ['recJobLoc']})
            company_container=child_soup.find('div' , {'class': ['sjcl']})
            company=company_container.div.span.text
            location=location_container.attrs['data-rc-loc']
            desc_container=child_soup.find('div' , {'class' :['summary']})
            try:
                desc= desc_container.ul.li.text
            except AttributeError:
                desc = ""
            
            if  role.upper() in str(title).upper().strip():
                all_data[ID]= [title , company.strip() , location ,desc,  href ]
            
                
    def getrole(self, role, location): 
        result, dups={} , set()
        if "," in location:
            location=location.split(',')
            if len(location)>=2:
                location= location[0].strip()+ "," + location[1].strip()
        url_first='https://www.indeed.com/jobs?q=' +role +'&l=' + location
        url='https://www.indeed.com/jobs?q=' +role +'&l=' + location + "&start="
        allproxies=self.getproxies()
        print(allproxies[1])
        threads= [ Thread(target=Indeed().get_indeed, args=( url +str(n) , role, self.get_session(allproxies), allproxies ),daemon=True) for n in range(1, 10)]
        threads.append(Thread(target=Indeed().get_indeed,  args=( url_first , role, self.get_session(allproxies), allproxies ),daemon=True))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        #cleaning the data
        for k, v in all_data.items():
            if k not in dups:
                result[k]=v 
                dups.add(k)
        all_data.clear()
        return result

    #Utility methods for proxies 
    @staticmethod
    def getproxies():
        url = "https://free-proxy-list.net/"
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        proxies = []
        for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                host = f"{ip}:{port}"
                proxies.append(host)
            except IndexError:
                continue
        return proxies
    @staticmethod
    def get_session( proxies):
        proxy = random.choice(proxies)
        #yield {"http": proxy, "https": proxy}
        return {"http": proxy, "https": proxy}




if __name__ == "__main__":
    Indeed().getrole('python', 'new york')
    #Indeed().getproxies()