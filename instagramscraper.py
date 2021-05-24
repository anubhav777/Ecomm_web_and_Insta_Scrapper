from selenium import webdriver
import time
from bs4 import BeautifulSoup 
import json
import requests

def instagram_user():
    browser=webdriver.Chrome()
    url='https://www.instagram.com/'
    browser.get(url)
    time.sleep(2)
    username_xpath="//input[contains(@name,'username')]"
    password_xpath="//input[contains(@name,'password')]"
    login_xpath="//div[contains(text(),'Log In')]"

    username=browser.find_element_by_xpath(username_xpath)
    password=browser.find_element_by_xpath(password_xpath)
    login=browser.find_element_by_xpath(login_xpath)
    new_login=login.find_element_by_xpath('..')
    username.send_keys(os.environ.get('USER_EMAIL))
    password.send_keys(os.environ.get('USER_EMAIL_PASSWORD))
    login.click()
    time.sleep(3)
    loc=browser.current_url
    if 'account' in loc:
        not_now_xpath="//button[contains(text(),'Not Now')]"
        not_now=browser.find_element_by_xpath(not_now_xpath)
        not_now.click()
    else:
        pass
        print('hi')
    time.sleep(4)
    src=browser.page_source
    soup=BeautifulSoup(src,'lxml')
    body=soup.find('body')
    script=body.find_all('script')
    main_script=None
    for i in range(len(script)):
        st=str(script[i])
        if 'window.__additionalDataLoaded' in st:
            main_script=st
        else:
            print('pssy')
    new_script=main_script.split(",",1)[1].rsplit(")",1)[0]
    new_data=json.loads(new_script)
    parent=new_data['user']
    id=parent['id']
    username=parent['username']
    profile_pic=parent['profile_pic_url']
    timeline_data=parent['edge_web_feed_timeline']['edges'][0]['node'].keys()
    print(id,username,profile_pic,timeline_data)


   
instagram_user()
# def user_post():
#     base_url='https://www.instagram.com/'
#     Search_query='amazing.python'
#     url=f"{base_url}{Search_query}/?hl=en"
#     browser.get(url)
#     lenOfPage =browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     source = browser.page_source
#     data=BeautifulSoup(source, 'html.parser')
#     body = data.find('body')
#     time.sleep(2)
#     script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
#     script_split=str(script).split(">")[1].strip('\n').replace('</script','').split("=",1)[1]
#     new_data=script_split[-1:]
#     if new_data !='}':
#         script_split=script_split.replace(new_data,'')
#     script_data=json.loads(script_split)
#     # entry_key=script_data['entry_data']
#     # timeline_data=entry_key['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
#     print(script_data)

# user_post()

# def recent_25_posts():
#     """With the input of an account page, scrape the 25 most recent posts urls"""
#     url = "https://www.instagram.com/" + 'amazing.python' + "/"
#     browser.get(url)
#     post = 'https://www.instagram.com/p/'
#     post_links = []
#     while len(post_links) < 55:
#         links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
#         for link in links:
#             if post in link and link not in post_links:
#                 print(link)
#                 post_links.append(link)
#         scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
#         browser.execute_script(scroll_down)
#         time.sleep(10)
#     else:
#         return post_links[:55]
        
#     print(len(post_links))
# # recent_25_posts()
