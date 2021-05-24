import requests,lxml
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import time
import requests
from selenium import webdriver
from fake_useragent import UserAgent
import random

ua = UserAgent(use_cache_server=False)
glob_end_cursor=''
cs=['nXLFxW9lmode0nfNdg95S1Kw3UgvtbSL','EmzuANMqTJ7QTKpPNWw0MpOe1pHaxiXo','y0hnj5ml7DJIGjSe5ghEOnMAuMKbJbfm','D20KHsn1PNaTxYqcvNakSiBMgFiL2GFY','TPKaituEtItcFXyWGIHJqlpQ7S9ds9Qp','EDPREh9gTEScBBlt8IJapz0RFnCiwLjL','k39hNB6ck1gAz78BCbMqcI993LdrS8BM','EJvKZm5dMYq2txR5Jvq1DANDSbL5oyX6','qiYWpQcwREQzg966Yn5JgS33T9OkYYoV']
def rand():
    url='https://www.sslproxies.org/'
    headers={
        'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://www.wikipedia.org/',
            'Connection': 'keep-alive',
    }
    random_ip = []
    random_port = []
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

        
    for x in soup.findAll('td')[::8]:
            random_ip.append(x.get_text())

    for y in soup.findAll('td')[1::8]:
            random_port.append(y.get_text())
        
    z = list(zip(random_ip,random_port))
    
    number = random.randint(0, len(z)-50)
    ip_random = z[number]

    ip_random_string = "{}:{}".format(ip_random[0],ip_random[1])

    proxy = {"http":'http://'+ip_random_string,'https':'https://'+ip_random_string}

    return proxy
# print(rand())
def insta_header(id,token,url,end_cursor='None',typ='None'):
    if typ == 'user':
        path='/graphql/query/?query_hash=6ff3f5c474a240353993056428fb851e&variables=%7B%22shortcode%22%3A%22'+id+'%22%2C%22include_reel%22%3Atrue%2C%22include_logged_out%22%3Afalse%7D'
    elif typ == 'comment':
        path='/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables=%7B%22shortcode%22%3A%22'+id+'%22%2C%22first%22%3A12%2C%22after%22%3A%22'+end_cursor+'%3D%3D%22%7D'
        
    else:
        path='/graphql/query/?query_hash=15bf78a4ad24e33cbd838fdb31353ac1&variables=%7B%22id%22%3A%22'+id+'%22%2C%22first%22%3A12%2C%22after%22%3A%22'+end_cursor+'%3D%3D%22%7D'
    headers={'authority': 'www.instagram.com',
                    'method': 'GET',           
                    'scheme': 'https',
                    'accept': '*/*',
                    'path': path,
                    'accept-language': 'en-US,en;q=0.9',
                    'cookie':'csrftoken='+random.choice(cs)+'; rur=ATN; mid=XwST2AALAAG76OTA3nFyEev8orDZ; urlgen="{\"27.34.68.231\": 17501}:1jspT7:lTFDTdgZ5IlQ7C1ChAWqffnLxE8"',
                    'referer': url,
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': ua.random,
                    'viewport-width': '767',}
    return headers
def tryop(shortcode,token):
    new_url= 'https://www.instagram.com/p/'+shortcode+'/'
    header=insta_header(shortcode,token,new_url,'None','user')
    
    url='https://www.instagram.com/graphql/query/?query_hash=6ff3f5c474a240353993056428fb851e&variables=%7B%22shortcode%22%3A%22'+shortcode+'%22%2C%22include_reel%22%3Atrue%2C%22include_logged_out%22%3Afalse%7D'
   
    proxy=rand()
    r=requests.get(url,proxies=proxy,headers=header,timeout=8)
    new_json=json.loads(r.text)
    parent=new_json['data']['shortcode_media']['owner']['reel']['owner']
    profile_pic=parent['profile_pic_url']
    username=parent['username']
    newobj={'username':username,'profile_pic':profile_pic}
    
    return newobj

def request_data(id,token,url,cursor,typ):
    end_cursor=cursor
    has_next_page=True
    newarr=[]
    
    while has_next_page != False:
        new_url=None
        if typ == 'page':
            new_url='https://www.instagram.com/graphql/query/?query_hash=15bf78a4ad24e33cbd838fdb31353ac1&variables=%7B%22id%22%3A%22'+id+'%22%2C%22first%22%3A12%2C%22after%22%3A%22'+end_cursor+'%3D%3D%22%7D'
        else:
            new_url='https://www.instagram.com/graphql/query/?query_hash=c769cb6c71b24c8a86590b22402fda50&variables=%7B%22tag_name%22%3A%22'+id+'%22%2C%22first%22%3A9%2C%22after%22%3A%22'+end_cursor+'%3D%3D%22%7D'
        header=insta_header(id,token,url,end_cursor)
        proxy=rand()
        datas=requests.get(new_url,proxies=proxy,headers=header,timeout=8)
        new_json=json.loads(datas.text)
        parent=None
     
        if typ == 'page':
            parent=new_json['data']['user']['edge_owner_to_timeline_media']
        else:
            parent=new_json['data']['hashtag']['edge_hashtag_to_media']
        end_cursor=parent['page_info']['end_cursor']
        has_next_page=parent['page_info']['has_next_page']

        if end_cursor != None:
            end_cursor=end_cursor.replace("=",'')
        else:
            pass
        timeline_code=timeline(parent,'recent',typ,token)
        newarr.extend(timeline_code)
    return newarr
def comment_filter(shortcode,cursor,token):
    cursor=cursor
    has_next_page=True
    newarr=[]
    all_data=[]
    while has_next_page != False:
    
        url='https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables=%7B%22shortcode%22%3A%22'+shortcode+'%22%2C%22first%22%3A12%2C%22after%22%3A%22'+cursor+'%3D%3D%22%7D'
        path='https://www.instagram.com/p/'+shortcode+'/'
        header=insta_header(shortcode,token,path,cursor,'comment')
        proxy=rand()
        r=requests.get(url,proxies=proxy,headers=header,timeout=8)
        new_json=json.loads(r.text)
        print(new_json)
        parent=new_json['data']['shortcode_media']['edge_media_to_parent_comment']
        total=parent['count']
        all_com=parent['edges']
        # print(new_json)
        comm_data=comment_data(all_com)
        new_cursor=parent['page_info']['end_cursor']
        if new_cursor != None:
            cursor=new_cursor.replace("=",'')
        
     
        has_next_page=parent['page_info']['has_next_page']
    
        all_data.extend(comm_data)
    return(all_data)
 


    # print(r.text)
    # newarr=[]
    # url=f"https://www.instagram.com/p/{shortcode}/"
    # source=requests.get(url).text
    # soup=BeautifulSoup(source,'lxml')
    # scripts=soup.find_all('script')
    # # for i in range(len(scripts)):
    # #     st=str(scripts[i])
    # #     if 'window.__additionalDataLoaded' in st:
    # #         print('hi')
    # #     else:
    # #         print('ni')
    # print(scripts[6])
    
    

# comment_filter('CCLcIh7ACyN')
def comment_comp(obj):
    parent=obj
    comm_id=parent['id']
    comm_text=parent['text']
    uploadeddate=parent['created_at']
    new_date=datetime.fromtimestamp(uploadeddate)
    start_date=new_date.strftime("%Y-%m-%d, %H:%M:%S")
    owner=parent['owner']
    owner_id=owner['id']
    profile_pic=owner['profile_pic_url']
    username=owner['username']
    comm_like=0
    try:
            comm_like=parent['edge_liked_by']['count']
    except:
            pass    
    newobj={'comm_id':comm_id,'comm_text':comm_text,'start_date':start_date,'owner_id':owner_id,'profile_pic':profile_pic,'username':username,'comm_like':comm_like}
    return newobj

def comment_data(obj):
    new_arr=[]
    for i in range(len(obj)):
        reply_obj=[]
        parent=obj[i]['node']
        child=comment_comp(parent)
        reply=parent['edge_threaded_comments']
        replied_comm=reply['count']
        replied_arr=reply['edges']
        
        if replied_comm >= 1:
            for j in range(len(replied_arr)):
                reply_parent=replied_arr[j]['node']
                reply_child=comment_comp(reply_parent)
                reply_obj.append(reply_child)

        
        new_arr.append({'comment':child,'reply':reply_obj, 'replied_comm':replied_comm})
    return new_arr
    # print(obj)

def text_filter(text):
    text=re.sub(r'\n','',text)
    text=text.replace(u'\xa0', u' ')
    return text
def page_profile(obj):
    id=obj['id']
    discription=obj['biography']
    followers=obj['edge_followed_by']['count']
    following=obj['edge_follow']['count']
    name=obj['username']
    profilepic=obj['profile_pic_url']

    
    newobj={'id':id,'name':name,'discription':discription,'followers':followers,'following':following,'profilepic':profilepic}
  
    return newobj
    
    
def timeline(obj,typ,cat='User',token='None',cur='None'):
    # number_of_post=obj['count']
    parent_post=obj['edges']
    new_arr=[]

    try:
        
        for i in range(len(parent_post)):
            comment_arr='None'
            try:
                comment_arr=parent_post[i]['node']['edge_media_to_comment'].keys()
            except :
                pass
            child=parent_post[i]['node']
            # print(child)
            postid=child['id']
            uploadeddate=child['taken_at_timestamp']
            new_date=datetime.fromtimestamp(uploadeddate)
            start_date=new_date.strftime("%Y-%m-%d, %H:%M:%S")
            post_text="No text"
            comment=0
            post_like=0
            owner_name='None'
            owner_profile='None'
            profile_picture=None
            shortcode=child['shortcode']
            print(shortcode)
            all_comment='Not avilable'
            if cat == 'main':
                profile_picture=child['display_url']
                owner_profile=child['owner']['profile_pic_url']
                owner_name=child['owner']['username']
            elif cat == 'hash':
                profile_picture=child['thumbnail_src']
                owner_func=tryop(shortcode,token)
                owner_name=owner_func['username']
                owner_profile=owner_func['profile_pic']

            else:
                profile_picture=child['thumbnail_src']
                owner_name=child['owner']['username']
            try:
                comment=child['edge_media_to_comment']['count']
                post_like=child['edge_media_preview_like']['count']
                post_text=child['edge_media_to_caption']['edges'][0]['node']['text']
            except:
                pass
            if cat == 'main':
                if child['edge_media_preview_comment']['count'] >= 1 :
                    cursor=child['edge_media_preview_comment']['page_info']['end_cursor']
                    new_cursor=cursor.replace("=",'')
                    all_comment=comment_filter(shortcode,new_cursor,token)
            else:
                pass
                # if 'page_info' in comment_arr:
                #     # all_comment=comment_filter(child['edge_media_to_comment']['edges'])
                #     # all_comment=comment_filter(shortcode)
                #     cursor=child['edge_media_to_comment']['page_info']['end_cursor']
                #     if i== 0:
                #         glob_end_cursor=child['edge_media_to_comment']['page_info']['end_cursor']
                #     if cursor != None:
                #             new_cursor=cursor.replace("=",'')
                #             all_comment=comment_filter(shortcode,new_cursor,token)
                # else:
                
                #     if comment >=1:
                #         all_comment=comment_filter(shortcode,cur,token)
            new_text=text_filter(post_text)
            
            media_type=None
            media_data=child['is_video']
            media_status=None
            post_status=typ
            if media_data == False:
                media_type="Image"
                media_status='No status'
            else:
                media_type="Video"
                media_status=child["video_view_count"]
           
           
            newobj={'postid':postid,'created_date':start_date,'post_text':new_text,'post_like':post_like,'comment':comment,'post_picture':profile_picture,'media_type':media_type,'media_status':media_status,'post_status':post_status,'owner_name':owner_name,'owner_profile':owner_profile,'all_comment':all_comment}
            
            new_arr.append(newobj)
            
    except Exception as e:
        print('err in',e)
    return new_arr

        
def instagram():
    newarr=[]
    base_url='https://www.instagram.com/'
    Search_query='amazing.python'
    url=f"{base_url}{Search_query}/"
    source=requests.get(url).text
    soup=BeautifulSoup(source,'lxml')
    header=soup.select_one('script[type="application/ld+json"]')
    new_header=str(header).split(">")[1].strip('\n').replace('</script','')
    parent=json.loads(new_header)
    all_script=soup.select('script[type="text/javascript"]')[3]
    script_split=str(all_script).split(">")[1].strip('\n').replace('</script','').split("=",1)[1]
    new_data=script_split[-1:]
    if new_data !='}':
        script_split=script_split.replace(new_data,'')
    script_data=json.loads(script_split)
    token=script_data['config']['csrf_token']
    entry_key=script_data['entry_data']
    entry_page_details=entry_key['ProfilePage'][0]['graphql']['user']
    page_data=page_profile(entry_page_details)
    timeline_data=entry_key['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
    end_cursor=entry_page_details['edge_owner_to_timeline_media']['page_info']['end_cursor']
    end_cursor=end_cursor.replace("=",'')
    timeline_code=timeline(timeline_data,'recent','User',token,'QVFBWm1nSDNHR3VfU1ZwSHkzLUN2eFptTGtiLVUxSkdGZS1KcTVXWVZCNTVXMW1URXd0Y3I3d0JXMTUxNU50cHZyUnJMalJQeEV0QmtxRnRqaUt3SHNCOA')
    cs.append(token)
    id=entry_page_details['id']

   

    extra_post=request_data(id,token,url,end_cursor,'page')
    # print(timeline_code)
 

    # page_name=parent['alternateName']
    # description=parent['description']
    # page_id=parent['@id']
    # followers=parent['userInteractionCount']
    # profile_img=parent['image']
    # newobj={'page_name':page_name,'description':description,'page_id':page_id,'followers':followers,'profile_img':profile_img}
    # newarr.append(newobj)
    # return newarr

# instagram()
# def tok_generator():
#     while len(cs) != 100:
#         base_url='https://www.instagram.com/'
#         Search_query='python.learning'
#         url=f"{base_url}{Search_query}/"
#         source=requests.get(url).text
#         soup=BeautifulSoup(source,'lxml')
#         header=soup.select_one('script[type="application/ld+json"]')
#         new_header=str(header).split(">")[1].strip('\n').replace('</script','')
#         parent=json.loads(new_header)
#         all_script=soup.select('script[type="text/javascript"]')[3]
#         script_split=str(all_script).split(">")[1].strip('\n').replace('</script','').split("=",1)[1]
#         new_data=script_split[-1:]
#         if new_data !='}':
#             script_split=script_split.replace(new_data,'')
#         script_data=json.loads(script_split)
#         token=script_data['config']['csrf_token']
#         cs.append(token)
#         print(len(cs))
#     instagram()
# tok_generator()

# print(random.choice(cs))
def hash_profile(obj):
    hash_id=obj['id']
    username=obj['name']
    profile_pic=obj['profile_pic_url']
    no_of_post=obj['edge_hashtag_to_media']['count']
    newobj={'hash_id':hash_id,'username':username,'profile_pic':profile_pic,'no_of_post':no_of_post}
    return newobj


def hash_search():
    base_url='https://www.instagram.com/'
    Search_query='trump'
    url=f"{base_url}explore/tags/{Search_query}/"
   
    source=requests.get(url).text
    soup=BeautifulSoup(source,'lxml')
    all_script=soup.select('script[type="text/javascript"]')[3]
    script_split=str(all_script).split(">")[1].strip('\n').replace('</script','').split("=",1)[1]
    new_data=script_split[-1:]
    if new_data !='}':
        script_split=script_split.replace(new_data,'')
    script_data=json.loads(script_split)
    entry_key=script_data['entry_data']
    token=script_data['config']['csrf_token']
    header=entry_key['TagPage'][0]['graphql']['hashtag']
    end_cursor=header['edge_hashtag_to_media']['page_info']['end_cursor']
    end_cursor=end_cursor.replace("=",'')
    user_details=hash_profile(header)
    timeline_header=entry_key['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']
    # timeline_data=timeline(timeline_header,'recent','hash',token,end_cursor)
    top_header=entry_key['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']
    
    top_data=timeline(top_header,'top','hash',token,end_cursor)
    
    # all_post=request_data(Search_query,token,url,end_cursor,'hash') 

    
   
  
hash_search()

# def user_timeline(obj):
#      for i in range(obj):
       
#             child=parent_post[i]['node']
#             postid=child['id']
#             uploadeddate=child['taken_at_timestamp']
#             new_date=datetime.fromtimestamp(uploadeddate)
#             start_date=new_date.strftime("%Y-%m-%d, %H:%M:%S")
#             post_text="No text"
#             comment=0
#             post_like=0
#             try:
#                 comment=child['edge_media_to_comment']['count']
#                 post_like=child['edge_media_preview_like']['count']
#                 post_text=child['edge_media_to_caption']['edges'][0]['node']['text']
#             except:
#                 pass
#             new_text=text_filter(post_text)
#             profile_picture=child['thumbnail_src']
#             media_type=None
#             media_data=child['is_video']
#             media_status=None
#             post_status=typ
#             if media_data == False:
#                 media_type="Image"
#                 media_status='No status'
#             else:
#                 media_type="Video"
#                 media_status=child["video_view_count"]
             
#             newobj={'postid':postid,'created_date':start_date,'post_text':new_text,'post_like':post_like,'comment':comment,'profile_picture':profile_picture,'media_type':media_type,'media_status':media_status,'post_status':post_status}
            
#             new_arr.append(newobj)


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
    token_script=None
    for i in range(len(script)):
        st=str(script[i])
        if 'window.__additionalDataLoaded' in st:
            main_script=st
        elif 'csrf_token' in st:
            token_script=st
        else:
            pass
    new_script=main_script.split(",",1)[1].rsplit(")",1)[0]
    token_script=token_script.split("=",1)[1].split("=",1)[1].rsplit(";",1)[0]
    new_token=json.loads(token_script)
    token=new_token['config']['csrf_token']
    new_data=json.loads(new_script)
    parent=new_data['user']
    id=parent['id']
    username=parent['username']
    profile_pic=parent['profile_pic_url']
    timeline_data=parent['edge_web_feed_timeline']
    end_cursor=timeline_data['page_info']['end_cursor']
    end_cursor=end_cursor.replace("=",'')
  
    all_timeline=timeline(timeline_data,'recent','main',token,end_cursor)


# instagram_user()



# tryop()
