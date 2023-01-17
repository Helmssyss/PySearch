from ..util.constants import headers
from bs4 import BeautifulSoup
from typing import Optional
import threading
import requests

class GoogleSearch:
    __lock = threading.Lock()
    __threads:list[threading.Thread] = []
    def __init__(self,query:Optional[str]=None,page:Optional[int]=None) -> None:
        self.page:Optional[str] = page
        self.query:Optional[str] = query
        self.__links:list[str] = []

    def __enter__(self):
        return self
    
    def __exit__(self,*args):
        self.__links.clear()
        self.__threads.clear()
    
    def __delete__(self):
        self.__links
        self.__lock
        self.__threads
    
    def __getCookie(self) -> dict:
        __result = requests.get("https://www.google.com/",headers=headers)
        __cookies = __result.cookies.get_dict()
        return __cookies
    
    def __searchQuery(self,slot):
        params = {
            "q" : self.query,
            "start": slot
        }
        response = requests.get("https://www.google.com/search",params=params,headers=headers,cookies=self.__getCookie())
        soup = BeautifulSoup(response.content,"lxml")
        for i in  soup.find_all("div",attrs={"class":"yuRUbf"}):
            self.__lock.acquire()
            link = i.a["href"]
            self.__links.append(link)
            self.__lock.release()
            
    @property
    def links(self) -> list[str]:
        for p in range(0, self.page*10 if self.page == 1 else (self.page) * 10, 10):
            # self.__searchQuery(p)
            t = threading.Thread(target=self.__searchQuery,args=(p,))
            t.start()
            self.__threads.append(t)
        
        for thread in self.__threads:
            thread.join()
        
        return self.__links
