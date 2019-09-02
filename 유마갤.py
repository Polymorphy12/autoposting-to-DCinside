from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests


start_time = time.time() 
#여기서부터 데이터 파싱하기.

#게시글 클래스.
class myPost:
    def __init__(self, posts_index):

        self._username= ""
        self.url = ""
        self.title = ""
        self.views = ""
        self.hits = ""

        
        notice_or_post = posts_index.find("td", {"class":"t_notice"})
        if notice_or_post.text != "공지":

            before_info_soup = posts_index.find("td", {"class":"t_subject"})
            info_soup = posts_index.find("a")

            #게시글의 제목과 주소 찾아서 설정하기
            self.url = info_soup["href"]
            self.title = info_soup.text

            #print("제목 : " + self.title + "\n주소 : " + self.url)

            #닉네임 찾아서 설정하기
            user_name = posts_index.find("td", {"class":"t_writer user_layer"})
            spans = user_name.find_all("span")
            
            for span in spans:
                self._username += span.text

            #print("닉네임 : " + self._username)
                
            
            #조회수와 추천수 찾아서 설정하기
            views_and_hits = posts_index.find_all("td", {"class":"t_hits"})
            arr = []
            for v_and_h in views_and_hits:
                arr.append(  v_and_h.text )
            self.views = arr[0]
            self.hits = arr[1]
            



#글쓴 사람 클래스.
class User:
    def __init__(self, name):
        self.name = name
        self.a = 5
        self.posts = []

    #이 사람이 쓴 게시글을 추가한다.
    def addPost(self, post):
        self.posts.append(post)

    #이사람이 쓴 게시글(post)들의 총 추천수를 반환한다.
    def calcTotalHits(self):
        number = 0
        for post in self.posts:
            number += int(post.hits)

        return number

    #이 사람이 쓴 게시글의 수를 반환한다.
    def totalNumberOfPosts(self):
        return len(self.posts)

    #이사람이 쓴 게시글(post)들의 총 추천수를 반환한다.
    def calcTotalViews(self):
        number = 0
        for post in self.posts:
            number += int(post.views)

        return number
    #이사람이 쓴 모든 게시글(post)들을 출력한다.
    def showAllPosts(self):
        print(self.name+ "'s post..")
        for post in self.posts:
            print("      " +post.title)

    
    #이사람이 쓴 모든 게시글(post)들을 반환한다.
    def returnAllPosts(self):
        s = ""
        s+= self.name+ "'s post..\n"
        for post in self.posts:
            s+="      " +post.title+"\n"
        return s


        

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


a = range(1,30)

userArray = []
userNameArray = []

for i in a:
    
    URL = "http://gall.dcinside.com/mgallery/board/lists/?id=unist2009&page="+str(i)    
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
            new_post = myPost(posts_index)
        
            if userNameArray.count(new_post._username) == 0 :
                userNameArray.append(new_post._username)
                tempUser = User(new_post._username)
                tempUser.addPost(new_post)
                userArray.append(tempUser)
            else:
                userArray[userNameArray.index(new_post._username)].addPost(new_post)
        

outputString = ""

for users in userArray:
    outputString += "아이디 : " + users.name + ", 총 받은 추천수: " + str(users.calcTotalHits()) + ", 총 조회수: " +str(users.calcTotalViews()) + ", 총 게시글 수: " + str(users.totalNumberOfPosts()) +"\n"
    print("아이디 : " + users.name + ", 총 받은 추천수: " + str(users.calcTotalHits()) + ", 총 조회수: " +str(users.calcTotalViews()) + ", 총 게시글 수: " + str(users.totalNumberOfPosts()) +"\n")
    outputString+=users.returnAllPosts()
    print(users.returnAllPosts())
    outputString+= "\n"


outputString += "--- %s seconds ---" %(time.time() - start_time)

#여기까지 데이터 파싱하기.



##
##options = webdriver.ChromeOptions()
####options.add_argument('headless')
##options.add_argument('window-size=1920x1080')
##options.add_argument("disable-gpu")
##
##
##options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")
##
##
##driver = webdriver.Chrome('C:/Users/Sumin/Desktop/study/chromedriver', chrome_options=options)
####driver = webdriver.Chrome('C:/Users/Sumin/Desktop/study/chromedriver')
###웹 자원 로드를 위해 3초까지 기다려준다.
##driver.implicitly_wait(1)
##
##
##driver.get('http://gall.dcinside.com/board/write/?id=food')
##
##driver.find_element_by_name('name').send_keys('ddddd')
##driver.find_element_by_name('password').send_keys('asdfzxcvasdfzxcv')
##driver.find_element_by_name('subject').send_keys("너희들이 쓴글들이야")
##
##
##
##
##driver.switch_to_frame(driver.find_element_by_id("tx_canvas_wysiwyg"));
##
###iframe 내부의 요소를 다룰 수 있다.
##
##
##print(outputString)
##driver.find_element_by_class_name('tx-content-container').send_keys(outputString)
##
##
##driver.switch_to_default_content()
##
##
##time.sleep(1)
##
##driver.find_element_by_xpath("//p[@class='btn_box_right']/input")
##
##time.sleep(5)
##
##driver.close()
##driver.quit()
##
###다시 iframe 외부를 다룬다.
##

##user_agent = driver.find_element_by_css_selector('#user-agent').text
##
##print('User-Agent: ', user_agent)
##
##driver.quit()
