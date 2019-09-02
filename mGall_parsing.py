from bs4 import BeautifulSoup
import requests

def get_html(url):
    _html = ""
    headers = {
    "User-Agent": "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        _html = response.text
    return _html


a = range(1,10)

for i in a:
    URL = "http://gall.dcinside.com/mgallery/board/lists/?id=unist2009&page="+str(i)
    html = get_html(URL)

    webtoon_list = list()

    soup = BeautifulSoup(html, 'html.parser')

    l = soup.find_all("a")

    print(len(l))

    webtoon_area = soup.find("table"
                    ).find_all("td", {"class":"t_subject"})


    for webtoon_index in webtoon_area:
        
        info_soup = webtoon_index.find("a", {"class":)
        _url = info_soup["href"]
        _title = info_soup.text
        print(_title)

