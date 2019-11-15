from webdirectory import WebDirectory
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import unquote
import redis
import uuid
from time import gmtime, strftime, time, sleep

class Yelp(WebDirectory):

    def __init__(self):
        self.home_url = "https://www.yelp.com" 
        self.redis = redis.Redis(host='localhost', port=6379, db=1,charset="utf-8", decode_responses=True)
        self.scaped = 0
        self.run_id = str(uuid.uuid4())

    def run(self):
        print("Running yelp search")
        print("Maxhits %s" % self.maxhits)
        run_data = {
            "time" : strftime("%H:%M:%S", gmtime()),
            "date" : strftime("%Y-%m-%d", gmtime()),
            "url" : self.home_url,
            "searchterm" : self.searchterm,
            "location" : self.location,
            "maxhits" : self.maxhits
        }
        self.redis.hmset("run:" + self.run_id, run_data)
        j=0
        while j <= int(self.maxhits):
            print("j=%d" % j)
            search_url = "https://www.yelp.com/search?find_desc=" + self.searchterm + "&find_loc=" + self.location + ("&start=%d" % j)
            urls = self.get_page(search_url,j)
            deduped = []
            for i in urls:
                if i not in deduped:
                    deduped.append(i)
            
            if len(deduped)==0:
                return

            for u in deduped:
                self.scrape_page(u)
                sleep(int(self.stealth_level))
                j=j+1

    def get_page(self, search_url, page): 
        page = super().get_page(search_url, page) 
        s_urls = page.select('a[href*="biz/"]')[:10]
        urls = [] 
        for u in range(len(s_urls)): 
            urls.append(self.home_url + s_urls[u]['href']) 
        return urls

    def scrape_page(self, page_url):
        page = super().get_page(page_url)
        scraped_data = {}
        #website url
        try:
            s_url = page.select('a[href*="biz_redir?url="]')[:1][0]
            a = BeautifulSoup(str(s_url),features="lxml")
            u = a.find('a',href=True)['href']
            assert(u.find('/biz_redir?url=')==0)
            r = unquote(u[u.find('=')+1:u.find('&')])
        except IndexError:
            r='No website'
        scraped_data['website'] = str(r)
        #name
        try:
            scraped_data['name'] = page.select('h1[class*="heading--"]')[0].text
        except Exception as e:
            print(str(e))
            scraped_data['name'] = str(e)
        print("Name = %s" % scraped_data['name'])
        #phone number
        try:
            p = page.find(text="Phone number").parent.nextSibling.string
        except Exception as e:
            p = 'No phone number'
        scraped_data['telephone'] = str(p)
        #address
        address_line_1 = ''
        address_town = ''
        address_post_code = ''
        
        try:
            address_line_1 = page.find("span", {"itemprop" : "streetAddress"}).contents[0]
        except:
            pass
        try:
            address_town = page.find("span", {"itemprop" : "addressLocality"}).contents[0]
        except:
            pass
        try:
            address_post_code = page.find("span", {"itemprop" : "postalCode"}).contents[0]
        except:
            pass
        scraped_data['address_line_1'] = str(address_line_1) or ''
        scraped_data['address_town'] = str(address_town) or ''
        scraped_data['address_post_code'] = str(address_post_code) or ''
        lead_id = str(uuid.uuid4())
        try:
            self.redis.hmset("lead:" + lead_id, scraped_data)
        except Exception as e:
            print(str(e))
            pass
        try:
            self.redis.sadd("leads",lead_id)
        except Exception as e:
            print(str(e)) 
            pass
        try:
            self.redis.zadd("idx_lead_date:",{ lead_id : time() })
        except Exception as e:
            print(str(e))
            pass
        try:
            self.redis.zadd("idx_lead_run:",{ self.run_id + ':' + lead_id : 0 },nx=True)
        except Exception as e:
            print(str(e))
            pass
        
