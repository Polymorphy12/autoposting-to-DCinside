from selenium import webdriver
import time

options = webdriver.ChromeOptions()
##options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")


options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")


driver = webdriver.Chrome('C:/Users/Sumin/Desktop/study/chromedriver', chrome_options=options)
##driver = webdriver.Chrome('C:/Users/Sumin/Desktop/study/chromedriver')
#웹 자원 로드를 위해 3초까지 기다려준다.
driver.implicitly_wait(1)


driver.get('http://gall.dcinside.com/board/write/?id=food')

driver.find_element_by_name('name').send_keys('ddddd')
driver.find_element_by_name('password').send_keys('asdfzxcvasdfzxcv')
driver.find_element_by_name('subject').send_keys('사실 이거 테스트용 글이야')




driver.switch_to_frame(driver.find_element_by_id("tx_canvas_wysiwyg"));

#iframe 내부의 요소를 다룰 수 있다.


print(driver.page_source)
driver.find_element_by_class_name('tx-content-container').send_keys('2분 뒤에 자삭해야징')


driver.switch_to_default_content()


time.sleep(1)

driver.find_element_by_xpath("//p[@class='btn_box_right']/input").click()

time.sleep(5)

driver.close()
driver.quit()

#다시 iframe 외부를 다룬다.


##user_agent = driver.find_element_by_css_selector('#user-agent').text
##
##print('User-Agent: ', user_agent)
##
##driver.quit()
