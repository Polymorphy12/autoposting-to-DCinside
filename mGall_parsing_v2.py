from bs4 import BeautifulSoup
import requests
import time

start_time = time.time() 

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
                arr.append(  v_and_h.text)
            self.views = arr[0]
            self.hits = arr[1]
            
 
class User:
    def __init__(self, name):
        self.name = name
        self.a = 5
        self.posts = []

    def addPost(self, post):
        self.posts.append(post)
        
    def calcTotalHits(self):
        number = 0
        for post in self.posts:
            number += int(post.hits)

        return number

    def totalNumberOfPosts(self):
        return len(self.posts)

    def calcTotalViews(self):
        number = 0
        for post in self.posts:
            number += int(post.views)

        return number
    def showAllPosts(self):
        print(self.name+ "'s post..")
        for post in self.posts:
            print("      " +post.title)


##    def calcAverageHits(self):
##
##    def calc




        

def get_html(url):
    _html = ""
##    headers = {
##    "User-Agent": "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"
##    }
##    headers = {
##        'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5'
##    }


    headers= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
    ,"Upgrade-Insecure-Requests" : "1"
    , "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    , "Accept-Encoding" : "gzip, deflate"
    , "Accept-Language" : "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url, headers=headers)
    print(response.headers)
    
    if response.status_code == 200:
        _html = response.text
    return _html


a = range(1,100)

userArray = []
userNameArray = []

for i in a:

    URL = "http://gall.dcinside.com/board/lists/?id=programming"
    #URL = "http://gall.dcinside.com/mgallery/board/lists/?id=pebble&page="+str(i)
    #URL = "http://gall.dcinside.com/board/lists/?id=food&page="+str(i)
    #time.sleep(0.2)
    html = get_html(URL)

    webtoon_list = list()

    soup = BeautifulSoup(html, 'html.parser')

    l = soup.find_all("a")

    print(soup.prettify())
    print(len(l))

    posts_area = soup.find("table"
                    ).find_all("tr", {"class":"tb"})
    

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
        


for users in userArray:
    print("아이디 : " + users.name + ", 총 받은 추천수: " + str(users.calcTotalHits()) + ", 총 조회수: " +str(users.calcTotalViews()) + ", 총 게시글 수: " + str(users.totalNumberOfPosts()))
    users.showAllPosts()
    print("\n")


print("--- %s seconds ---" %(time.time() - start_time))
