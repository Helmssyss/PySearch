from ..util.constants import headers
import threading
import requests
from bs4 import BeautifulSoup
from typing import Optional


class BingSearch:
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
            __result = session.get("https://www.bing.com",headers=headers)
            __cookies = __result.cookies.get_dict()
            return __cookies

    def __searchQuery(self,slot):
        with requests.Session() as session:
            params = {
                'q' : self.query,
                "sp" : '1',
                "first" : slot
            }
            response = session.get("https://www.bing.com/search",params=params,headers=headers,cookies=self.__getCookie())
            soup = BeautifulSoup(response.content,"lxml")
            for s in soup.find_all("div",{"class":"b_title"}):
                self.__lock.acquire()
                try:
                    self.__links.append(s.a["href"])
                except:
                    pass
                finally:
                    self.__lock.release()
    @property
    def links(self) -> list[str]:
        threads:list[threading.Thread] = []
        for i in range(1, (self.page * 10) + 1,11):
            t = threading.Thread(target=self.__searchQuery,args=(i,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
    
        return self.__links
