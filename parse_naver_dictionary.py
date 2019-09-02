
from bs4 import BeautifulSoup
 
import urllib3
import urllib.parse
import urllib.request
 
def get_dic_search(word):
    url1 = "http://terms.naver.com/search.nhn?query="
    url2 = urllib.parse.quote_plus(word)
    FullURL = url1 + url2
    http = urllib3.PoolManager()
    response=http.request("GET",FullURL)
    print("호호1")
    soup = BeautifulSoup(response.data, "html5lib")
    print("호호2")
    result=""
    result += soup.find('dd',{'class':'dsc'}).get_text().encode('utf-8')

    print("호호3")
    a = soup.find('ul',{'class':'thmb_lst',}).find('li').find('dt').find('a')

    print("호호4")
    result += "\n[본문링크]\n"+"http://terms.naver.com"+a["href"].encode('utf-8')
 
    return result
 
word = input('무엇을 검색하시겠습니까? : ')
print("호호")
print (get_dic_search(word))
