import requests
import re
from urllib.parse import urlencode
from urllib.parse import urlsplit
import tldextract
from six.moves.urllib.parse import urlparse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from time import sleep
import nltk
import spacy

ua = UserAgent()
email_regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
crn = r"([a-zA-z]{2}\d{6})|(\d{8})"

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
    'style'
	# there may be more elements you don't want, such as "style", etc.
]

nlp = spacy.load("en_core_web_sm")

class SiteClassifier:
    def __init__(self,url):
        self.url = url
        self.parsedurl = urlparse(url)
        self.root = self.parsedurl.scheme + "://" + self.parsedurl.netloc
        ext = tldextract.extract(self.url)
        if (ext.subdomain!="www"):
            print("Is a sub domain, calculating tld")
            self.root = "http://www." + ext.domain + "." +  ext.suffix 
        self.roothtml = ''
        self.sitelinks = []
        self.excludedlinks = []
        self.socialmedialinks = []
        self.onlinedirectorylinks = []
        self.crns=[]
        self.about = ''
        self.aboutlink=''
        self.emails = []
        self.text = ''
        self.doc = None
        self.ent_labels = None

    def gohome(self):
        try:
            r = requests.get(self.root,{"User-Agent": ua.random})
            soup = BeautifulSoup(r.text, "html.parser")
            self.roothtml = r.text
            links = soup.find_all('a', href=True)
            for l in links:
                if l['href'][0:1]=="/":
                    newlink = self.root + l['href']
                    self.sitelinks.append(newlink)
                elif "http" not in l['href'].lower():
                    newlink = self.root + "/" + l['href']
                    self.sitelinks.append(newlink)
                elif tldextract.extract(self.root).domain.lower() == tldextract.extract(l['href']).domain.lower():
                    self.sitelinks.append(l['href'])
                else:
                    self.excludedlinks.append(l['href'])
            for e in self.excludedlinks:
                if "linkedin" in e.lower():
                    self.socialmedialinks.append(e)
                elif "facebook" in e.lower():
                    self.socialmedialinks.append(e)
                elif "twitter" in e.lower():
                    self.socialmedialinks.append(e)
                elif "instagram" in e.lower():
                    self.socialmedialinks.append(e)
        except Exception as e:
            print("siteclassifier.gohome : " + str(e))
        return

    def readallaboutit(self):
        try:
            aboutlinks = [s for s in self.sitelinks if "about" in s.lower()]
            aboutlink = (min(aboutlinks, key=len))
            self.aboutlink = aboutlink
            r = requests.get(aboutlink,{"User-Agent": ua.random})
            if len(r.text)==0:
                return
            soup = BeautifulSoup(r.text, 'html.parser')
            pagetext = soup.findAll(text=True)
            for textitem in pagetext:
                print(textitem)
                self.about += textitem
        except Exception as e:
            print("siteclassifier.readallaboutit " + str(e))
        return

    def findcompanyregno(self):
        soup = None
        try:
            for l in self.sitelinks:
                r = requests.get(l,{"User-Agent": ua.random})
                soup = BeautifulSoup(r.text, 'html.parser')
                pagetext = soup.findAll(text=True)
        
                output = ''
                for t in pagetext:
	                if t.parent.name not in blacklist:
		                output += '{} '.format(t)
        
                crns = re.findall(crn, output)
                crn_list = []
                if crn!=[]:
                    crn_list.extend(crns)
                for i in crn_list:
                    if i not in self.crns:
                        self.crns.append(i)
        except Exception as e:
            print("siteclassifier.findcompanyregno : " + str(e))
        finally:
            if soup:
                soup.decompose()
        return

    def findemailaddresses(self):
        soup = None
        try:
            for l in self.sitelinks:
                r = requests.get(l,{"User-Agent": ua.random})
                soup = BeautifulSoup(r.text, 'html.parser')
                emails = re.findall(email_regex, soup.text)
                if emails!=[]:
                    self.emails.extend(emails)
                emails=[]
        except Exception as e:
            print("siteclassifier.findemailaddress : " + str(e))
        finally:
            if soup:
                soup.decompose()
        return

    def url_to_string(self, url):
        res = requests.get(url,{"User-Agent": ua.random})
        html = res.text
        soup = BeautifulSoup(html, 'html5lib')
        for script in soup(["script", "style", 'aside']):
            script.extract()
        return " ".join(re.split(r'[\n\t]+', soup.get_text()))

    def striptext(self):
        soup = None
        #f=open("pagetext", "a+")
        try:
            output = ''
            for l in self.sitelinks:
                output += '{} '.format(self.url_to_string(l))
        #        f.write(output + "\r\n")
        #        output = ""
            self.text = output
        except Exception as e:
            print("siteclassifier.entityextraction : " + str(e))
        finally:
            if soup:
                soup.decompose()
        return

    def entityextraction(self):
        if len(self.text)==0:
            self.striptext()
        self.doc = nlp(self.text)
        self.ent_labels = [x.label_ for x in self.doc.ents]