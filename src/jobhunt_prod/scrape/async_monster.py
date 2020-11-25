'''
monster scrape with async design

changed url to for location of applying 
https://www.monster.com/jobs/search?q=python&where=new-york&jobid=220822592

'''

from bs4 import BeautifulSoup
from asyncio import gather, run
from aiohttp import ClientSession


alldata={}
async def get_monster(url, role):
    async with ClientSession() as session:
        async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as response:
            text= await response.text()
            soup = BeautifulSoup(text, 'html.parser')
            summary_container= soup.find_all('div', {'class': ['summary']})
            for i, container in enumerate(summary_container):
                title=None
                try:
                    title=container.h2.a.text #job title 
                    href=container.a['href'] #a tag href attribute within the title class 
                except:
                    pass
                if title is not None and role.upper() in str(title).upper().strip():
                    company=container.span.text
                    location = soup.find("span" , string=company).find_next("span").text.strip()
                    date = soup.find("span" , string=company).find_next("time").text.strip()
                    alldata[str(i) +   href] =[title,href, company, location, date]

async def getrole_monster(role, location):
    locate=location
    rawdata, result={}, {}
    if "," in location:
        location=location.split(',')
        if len(location)>=2:
            locate= location[0].strip()+ "," + location[1].strip()
                 
    url='https://www.monster.com/jobs/search/?q= ' +role+ '&where='+locate+' &stpage='
    url_end="&page=" 
    await gather(
        get_monster(url + str(1) +url_end+str(1),  role ),
        get_monster(url + str(2) +url_end+str(2), role),
        get_monster(url + str(3 )+url_end+str(3), role), 
        get_monster(url + str(4)+url_end+str(4), role),
        get_monster(url + str(5) +url_end+str(5), role ),
        get_monster(url + str(6) +url_end+str(6), role ),
        get_monster(url + str(7) +url_end+str(7), role), 
    )
    rawdata.update(alldata)
    for k, v in rawdata.items():
        if v not in result.values():
            result[k]=v 
    alldata.clear()

    return result


if __name__ == "__main__":
    getrole_monster('python' , 'New York')   

'''

get_monster(url + str(11) +url_end+str(11), role), 
get_monster(url + str(12) +url_end+str(12), role), 
get_monster(url + str(13 )+url_end+str(13), role), 
get_monster(url + str(14)+url_end+str(14), role), 
get_monster(url + str(15) +url_end+str(15), role), 
get_monster(url + str(16) +url_end+str(16), role), 
get_monster(url + str(8)+url_end+str(8), role), 
get_monster(url + str(9) +url_end+str(9), role), 
get_monster(url + str(10) +url_end+str(10), role), 


'''