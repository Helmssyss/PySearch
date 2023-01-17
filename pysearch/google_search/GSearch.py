from ..util.constants import headers
import threading
import requests
from bs4 import BeautifulSoup
from typing import Optional

class GoogleSearch:
    def __init__(self,query:Optional[str]=None,page:Optional[int]=None) -> None:
        self.page = page
        self.query = query
        self.__links:list[str] = []
        self.__lock = threading.Lock()

    def __enter__(self):
        return self
    
    def __exit__(self,*args):
        self.__links.clear()
    
    def __getCookie(self) -> dict:
        with requests.Session() as session:
            __result = session.get("https://www.google.com/",headers=headers)
            __cookies = __result.cookies.get_dict()
            return __cookies
    
    def __searchQuery(self,slot):
        with requests.Session() as session:
            params = {
                "q" : self.query,
                "start": slot
            }
            response = session.get("https://www.google.com/search",params=params,headers=headers,cookies=self.__getCookie())
            soup = BeautifulSoup(response.content,"lxml")
            for i in  soup.find_all("div",attrs={"class":"yuRUbf"}):
                self.__lock.acquire()
                self.__links.append(i.a["href"])
                self.__lock.release()
    @property
    def links(self) -> list[str]:
        threads:list[threading.Thread] = []
        for p in range(0, 10 if self.page == 1 else (self.page - 1) * 10,10):
            t = threading.Thread(target=self.__searchQuery,args=(p,))
            t.start()
            threads.append(t)
        
        for thread in threads:
            thread.join()
        
        return self.__links
