import requests
from bs4 import BeautifulSoup
import re
import js

class Quora_Crawler():

    '''
    basic crawler
    '''
    def __init__(self, url, option="print_data_out"):
        '''
        initialize the crawler
        '''

        self.option = option
        self.url = url
        self.header = {}
        self.header[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0"
#        self.header["Host"]="www.zhihu.com"
        self.header["Referer"] = "www.quora.com"
        # cookie
        self.cookies = js.result


    def send_request(self):
        '''
        send a request to get HTML source
        '''
        added_followee_url = self.url# + "/following"
        try:
            r = requests.get(added_followee_url, cookies=self.cookies,
                             headers=self.header, verify=False)
        except:
            re_crawl_url(self.url)
            return
        content = r.content
        print(content)
        if r.status_code == 200:
            self.parse_user_profile(content)
            #print(r.text)


    def parse_user_profile(self, html_source):
        '''
        parse the user's profile to mongo
        '''

        # initialize variances

        self.user_name = ''
        self.fuser_gender = ''
        self.user_location = ''
        self.user_followees = ''
        self.user_followers = ''
        self.user_questions=''
        self.user_answers = ''
        self.user_be_viewed = ''
        self.user_education_school = ''
        self.user_education_subject = ''
        self.user_employment = ''
        self.user_employment_extra = ''
        self.user_info = ''
        self.user_intro = ''

        soup = BeautifulSoup(html_source,'html.parser')

        self.user_name = soup.find('a',attrs={'class':'user'}).get_text()

        infoSession=soup.find('div',attrs={'class':'AboutSection'}).find('div',attrs={'class':'contents'})
        listofInfo=infoSession.find_all('span', attrs={'class': 'main_text'})

        for singleInfo in listofInfo:
            text = singleInfo.get_text()
            print(text,singleInfo.parent['class'])
            if text.startswith("Works at "):
                self.user_employment=text.replace("Works at ","",1)

            elif text.startswith("Lives in "):
                self.user_location = text.replace("Lives in ","",1)
            elif text.endswith(" answer views"):
                self.user_be_viewed = text.replace(" answer views","",1)
            elif text.startswith("Studied at "):
                self.user_education_school = text.replace("Studied at ","",1)
            elif singleInfo.parent.name=="div":
                if ('WorkCredentialListItem' in singleInfo.parent['class']):
                    self.user_employment = text
                elif ('SchoolCredentialListItem' in singleInfo.parent['class']):
                    self.user_education_school = text
        profileInfoSession = soup.find('div',attrs={'class':'EditableList NavList ProfileNavList'})
        listofProfileInfo = profileInfoSession.find_all('a')

        for singleProfileInfo in listofProfileInfo:
            text = singleProfileInfo.get_text()
            valueList = re.findall('[\d\,]+', text)
            value = valueList[0] if len(valueList)!=0 else ""
            if text.startswith("Answers"):
                self.user_answers = value
            elif text.startswith("Questions"):
                self.user_quetions = value
            elif text.startswith("Followers"):
                self.user_followers = value

            elif text.startswith("Following"):
                self.user_followees =value
        if self.option == "print_data_out":
            self.print_data_out()
        else:
            self.store_data_to_mongo()


     def print_data_out(self):
        '''
        print out the user data
        '''
        print("*" * 60)
        print('user name:%s\n' % self.user_name)
        print('address:%s\n' % self.user_location)
        print("questions:%s\n" % self.user_quetions)
        print("answers:%s\n" % self.user_answers)
        print("num of followers:%s\n" % self.user_followers)
        print("num of following:%s\n" % self.user_followees)
        print("work:%s\n" % self.user_employment)
        print("education:%s\n" % self.user_education_school)
        print("answer be viewed:%s" % self.user_be_viewed)
        print("*" * 60)

spider = Quora_Crawler(url='xxx')

spider.send_request()
