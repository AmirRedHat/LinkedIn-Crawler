import os 
import sys 
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__)))))
from crawler import *
from config import *
from database import *
from decorators import exceptionLog
# from selenium.webdriver import Chrome, ChromeOptions


# --------- CRAWLER

def testGetDriver():
   driver = getDriver()
   assert True

def dtestLogin():
   driver = getDriver()
   login("amir.ch.charehei1382@gmail.com", "pythonredhat", driver)
   sleep(10)
   assert True

def dtestLoginWithCookie():
   driver: Chrome = getDriver()
   driver.get(LOGIN_URL)
   is_valid, cookie = cookieIsValid()
   print(is_valid, cookie)
   driver.add_cookie(cookie)
   driver.refresh()
   sleep(2)
   driver.refresh()
   sleep(20)
   assert True

def dtestSearch():
   driver = getDriver()
   login(EMAIL, PASSWORD, driver)
   search(driver)
   assert True

def dtestProfileDetail():
   driver = getDriver()
   login(EMAIL, PASSWORD, driver)
   # link = "https://www.linkedin.com/in/hassan-noshadifar-3249a6203/"
   # link = "https://www.linkedin.com/in/mahdielyasi/"
   link = "https://www.linkedin.com/in/emami-owl-9a691086"
   details = getProfileDetail(link, driver)
   # storeProfileDetail([details])
   assert True

def dtestCompleteProfile():
   completeProfileDetails(True)
   assert True

def dtestExportDetails():
   exportDetailsAsJson()
   assert True

# --------- CRAWLER

# --------- DATABASE

def dtestInsertProfileData():
   result = None
   with open("C:/Users/amirc/OneDrive/Desktop/WorkSpace/Projects/Practice/Python/LinkedInCrawler/LinkedInCrawler/utils/test/output.json", "r") as _file:
      result = json.load(_file)

   detail_result = []
   with open("C:/Users/amirc/OneDrive/Desktop/WorkSpace/Projects/Practice/Python/LinkedInCrawler/LinkedInCrawler/utils/test/profile_output.json", "r") as _file:
      detail_result = json.load(_file)

   data = []
   for user in result["users"]:
      detected_details = [detail for detail in detail_result if detail["profile_link"] == user["profile_link"]]
      if detected_details:
         user["details"] = detected_details[0]
      
      data.append(user)

   insertProfileDetail(data)
   assert True


def dtestGetProfileLinks():
   links = getProfileLinks()
   print("https://www.linkedin.com/in/ali-soltani-071b32aa?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABdN5NUBW-fKwWfsPTFlXHybF2felhEZ4NI" in links)
   assert True


def dtestGetUncompletedProfiles():
   res = getUncompletedProfiles()
   print(res)
   print(res[0].profile_link)
   print(res[0].id)
   assert True


def dtestNestedProfileDetail():
   data = getNestedProfileDetail()
   print(data[0])
   assert type(data) == list

# --------- DATABASE

# --------- FREE MODULES

def dtestDecorators():

   @exceptionLog
   def raiseException(a, k1=2):
      raise Exception("invalid parameters")

   raiseException(1)

   assert True


def dtestMain():
   main(to_json=True)
   assert True