from abc import ABC, abstractmethod 
from bs4 import BeautifulSoup 
from threading import Thread 
from urllib.request import urlopen
  
class AbstractWebDirectory(ABC): 
  
    @property
    @abstractmethod
    def url(self): 
        pass

    @property
    @abstractmethod
    def searchterm(self): 
        pass

    @property
    @abstractmethod
    def location(self): 
        pass

    @property
    @abstractmethod
    def maxhits(self):
        pass 
    
    @abstractmethod
    def run(self):
        pass

class WebDirectory(AbstractWebDirectory):

    def __init__(self):
        self.__url = ''
        self.__searchterm = ''
        self.__location = ''
        self.__maxhits = 0
        self.__stealth_level = 0

    @property
    def url(self): 
        return self.__url
    
    @url.setter
    def url(self,url):
        self.__url = url

    @property
    def searchterm(self): 
        return self.__searchterm

    @searchterm.setter
    def searchterm(self, searchterm):
        self.__searchterm = searchterm

    @property
    def location(self): 
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location

    @property
    def maxhits(self):
        return self.__maxhits

    @maxhits.setter
    def maxhits(self, maxhits):
        self.__maxhits = maxhits

    @property
    def stealth_level(self):
        return self.__stealth_level

    @stealth_level.setter
    def stealth_level(self, stealth_level):
        self.__stealth_level = stealth_level

    @abstractmethod
    def run(self):
        pass

    def get_page(self, search_url, page=None):
        s_html = urlopen(search_url).read()  
        print("get_page %s" % search_url)
        soup_s = BeautifulSoup(s_html, "lxml") 
        return soup_s