#get_photos_from_gall_v1.py
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests


def get_html(url):
    _html = ""
##    headers = {
##    "User-Agent": "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
##    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    ,"Upgrade-Insecure-Requests" : "1"
    , "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    , "Accept-Encoding" : "gzip, deflate"
    , "Accept-Language" : "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    response = requests.get(url, headers=headers)
    #print("response code: ", response.status_code)
    #print(response.headers)
    if response.status_code == 200:
        _html = response.text
    return _html


def get_photo(referer_url, target_url):    
    _html = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    ,"Upgrade-Insecure-Requests" : "1"
    , "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    , "Accept-Encoding" : "gzip, deflate"
    , "Accept-Language" : "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(target_url, stream=True)
    print("response code: ", response.status_code , "\n")
    print(headers ,"\n")
    if response.status_code == 200:
        _html = response
    return _html



#4페이지만큼 디시인사이드 갤러리 파싱을 할것이다.
a = range(1,2)

userArray = []
userNameArray = []

for i in a:
    #URL = "http://gall.dcinside.com/mgallery/board/lists/?id=pebble&page="+str(i)
    URL = "http://gall.dcinside.com/board/lists/?id=food&page="+str(i)
    #time.sleep(0.2)
    html = get_html(URL)

    webtoon_list = list()

    soup = BeautifulSoup(html, 'html.parser')

    l = soup.find_all("a")

    print(len(l), URL)

    #print(soup.prettify())

    posts_area = soup.find("table").find_all("tr", {"class":"tb"})

    for posts_index in posts_area:

        notice_or_post = posts_index.find("td", {"class":"t_notice"})
        if notice_or_post.text != "공지":

            post_subject = posts_index.find("td", {"class":"t_subject"})
            #사진을 가지고 있는 게시물을 목록페이지에서 찾는다.
            a_tag_from_subject = post_subject.find("a", {"class": "icon_pic_n"})
            #현재 게시물이 사진을 가지고 있는 게시물이라면 if문을 수행한다.
            if(a_tag_from_subject):
                print(a_tag_from_subject.text)
                print(a_tag_from_subject["href"])

                #현재 게시물에 접근하여 HTML 문서를 가져온다.
                tempURL = "http://gall.dcinside.com/"+a_tag_from_subject["href"]
                tempHtml = get_html(tempURL)
                tempSoup = BeautifulSoup(tempHtml, 'html.parser')

                #가져온 HTML 문서에서 첨부된 사진들을 찾는다.
                uploadedFiles = tempSoup.find_all("li", {"class": "icon_pic"})

                for file in uploadedFiles:
                    file_name  = file.a.string + " "
                    file_extension = file_name[-4:-1]
                    #파일 주소를 가져온다.
                    file_link = file.a["href"]

                    a = "http://image.dcinside.com/viewimage.php"
                    b = "http://image.dcinside.com/download.php"

                    print(file_link.replace(b,a))

                    

                    try:
                        img_file = get_photo(tempURL, file_link.replace(b,a))
                        f = open("C:/Users/Sumin/Desktop/study/sample_img/food/"+file_name, 'wb')
                        print(img_file.raw)
                        f.write(img_file.raw.read())
                        print("!!!!!!!!!!!!!!!closed!!!!!!!!!!!!!!!!!!!!!!!!!")
                        f.close()
                    except Exception as e:
                        print( e)
                        pass
                

                
