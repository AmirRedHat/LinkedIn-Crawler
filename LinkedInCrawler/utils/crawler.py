from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))
from settings import *
import json
from time import sleep, time
from config import *
from decorators import exceptionLog
from log import writeLog
from database import *
import argparse


LOGIN_URL = "https://www.linkedin.com/uas/login"
SEARCH_KEYWORD = "https://www.linkedin.com/search/results/people/?keywords=%s&page=%s"
HIGHER_120_VERSION = "https://googlechromelabs.github.io/chrome-for-testing/"
LOWER_120_VERSION = "https://chromedriver.chromium.org/downloads"
RETRY = 3


def getDriver() -> Chrome:
   # check connection
   try:
      response = requests.get("https://google.com")
   except:
      raise Exception("[+] Connection Issue")


   path = os.path.abspath(DRIVER_PATH)
   options = ChromeOptions()
   options.add_argument("--disable-gpu")
   # to use tool on ubuntu server (reqirement packages must be install)
   # options.add_argument('--no-sandbox')
   # options.add_argument("--headless")
   
   # chromeService = ChromeService(executable_path=)
   # driver = Chrome(service=chromeService, options=options)
   
   try:
      driver = Chrome(executable_path=path, options=options)
   except Exception as e:
      print("[ERROR] %s" % e)
      print("[!] Maybe your chrome version and driver version not matched !")
      print("[-] Higher 120 version")
      print(HIGHER_120_VERSION)
      print("[-] Lower 120 version")
      print(LOWER_120_VERSION)
      
   return driver


def login(email: str, password: str, driver: Chrome):
   """
      login account using email and password and store cookies 
      :param email: str = valid email of linkedin account | in config.py
      :param password: str = password of linkedin account | in config.py
      :param driver: Chrome = selenium driver
   """
   driver.get(LOGIN_URL)
   is_valid, cookie = cookieIsValid()
   if is_valid:
      driver.add_cookie(cookie)
      driver.refresh()
      if "Feed" in driver.title:
         print("[+] Login process successfuly done !")
         return
      else:
         print("[!] Need to verify manually !")

   emailElement = driver.find_element(By.ID, "username")
   emailElement.send_keys(email)
   passwordElement = driver.find_element(By.ID, "password")
   passwordElement.send_keys(password)
   passwordElement.submit()
   sleep(100)
   storeCookie(driver.get_cookies())


def search(driver: Chrome, keyword: str = KEYWORD) -> list:
   """
      search for users that contain KEYWORD | default value is in config.py
      :param driver: Chrome = selenium driver | got from getDriver func
      :param keyword: str = the key word that want to search
   """
   # get existence profile links for remove duplicate values from result of search-engine
   exists_links = getProfileLinks()
   valid_users = list()
   page = 1
   count = 0
   while True:
      # MAX_PEOPLE is stored in settings.py
      if count >= MAX_PEOPLE:
         break
      
      try:
         driver.get(SEARCH_KEYWORD % (keyword, page))
         print("getting %s" % (SEARCH_KEYWORD % (keyword, page), ))
      except Exception as err:
         print("[!] ERROR in getting search page: ", str(err))
         driver.refresh()
         continue

      sleep(2)
      try:
         users = driver.find_elements(By.CLASS_NAME, "entity-result__item")
         page += 1
         for user in users:
            user_detail = user.text.split("\n")
            try:
               user_name = user_detail[0]
               user_skills = user_detail[4]
               user_location = user_detail[5]
               # get profile link
               user_profile = user.find_element(By.CLASS_NAME, "entity-result__universal-image")
               a_tag = user.find_element(By.TAG_NAME, "a")
               image_tag = user_profile.find_element(By.TAG_NAME, "img")
               profile_link = a_tag.get_attribute("href")
               if profile_link in exists_links:
                  continue

               profile_image = image_tag.get_attribute("src")
               if keyword.lower() in user_skills.lower():
                  valid_users.append({
                     "username": user_name,
                     "skills": user_skills,
                     "location": user_location,
                     "profile_link": profile_link,
                     "profile_image": profile_image
                  })
                  count += 1
            except IndexError:
               print(user_detail)
               continue

            except Exception as err:
               writeLog("[ERROR] error in second try block | error: %s" % (err,))
               continue

      except Exception as err:
         print("error in page %s : %s" % (page, err))
         writeLog("[ERROR] error in first try block | error: %s" % (err,))
         page += 1
         continue
   
   print("[+] Search and crawl process successfully done !")
   writeLog("[INFO] Search process successfuly completed | keyword: %s" % keyword)
   return valid_users


def store(data: dict, output: str = OUTPUT):
   with open(OUTPUT, "w") as _file:
      json.dump(data, _file)

   print("[+] Summary details saved !")


def storeProfileDetail(data: dict):
   with open(PROFILE_OUTPUT, "w") as _file:
      json.dump(data, _file)

   print("[+] Profile details saved !")


def storeCookie(cookies: dict):
   """ 
      store cookies in json file | after login process the cookies are useful
      :param cookies: dict = the cookies that got from driver after login process
   """
   with open(COOKIE_PATH, "w") as _file:
      json.dump(cookies, _file)
   print("[+] Cookies stored successfully !")


def cookieIsValid():
   """
      read cookies from json file and check login-key, if conditions are ok then return it
   """
   with open(COOKIE_PATH, "r") as _file:
      try:
         result = json.load(_file)
      except:
         return False, None

      is_valid = [i for i in result if i["name"] == "li_at" and i["expiry"] > time()]
      if len(is_valid) > 0:
         return True, is_valid[0]

      return False, None


def scroll_half(driver):
   driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

def scroll_bottom(driver):
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


@exceptionLog
def getExperiences(profile_link: str, driver: Chrome):
   url = profile_link.split("?")[0] + "/details/experience"
   driver.get(url)
   for _ in range(RETRY):
      try:
         main = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
         break
      except TimeoutException:
         print("[!] Loading took too much time!")
         sleep(1)

   scroll_half(driver)
   scroll_bottom(driver)

   for _ in range(RETRY):
      try:
         main = WebDriverWait(main, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'pvs-list')))
         break
      except TimeoutException:
         print("[!] Loading took too much time!")
         sleep(1)

   experience_details = list()
   experience = main.find_elements(By.TAG_NAME, "li")
   for li in experience:
      details = []
      splited = li.text.split("\n")[:12]
      if "Skills" in li.text and len(splited) <= 2:
         continue 

      for detail in splited:
         detail = detail.strip()
         if detail not in details:
            details.append(detail)

      if len(details) >= 3:
         position = details[0]
         company = details[1]
         date = details[3] if "time" in details[2].lower() else details[2]
         if "-" not in date and "·" not in date:
            continue 

         exp_detail = {
            "position": position,
            "company": company,
            "date": date
         }
         if exp_detail not in experience_details:
            experience_details.append(exp_detail)

   return experience_details


@exceptionLog
def getEducations(profile_link: str, driver: Chrome):
   url = profile_link.split("?")[0] + "/details/education"
   driver.get(url)
   for _ in range(RETRY):
      try:
         main = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
         break
      except TimeoutException:
         print("[!] Loading took too much time!")
         sleep(1)

   scroll_half(driver)
   scroll_bottom(driver)

   for _ in range(RETRY):
      try:
         main = WebDriverWait(main, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'pvs-list')))
         break
      except TimeoutException:
         print("[!] Loading took too much time!")
         sleep(1)

   education_details = list()
   try:
      education = main.find_elements(By.TAG_NAME, "li")
   except NoSuchElementException:
      return education_details

   for li in education:
      details = []
      splited = li.text.split("\n")[:12]

      for detail in splited:
         detail = detail.strip()
         if detail not in details:
            details.append(detail)

      if len(details) >= 3:
         name = details[0]
         desc = details[1]
         date = details[2]
         if "-" in date:
            start_at, end_at = date.split("-")
         else:
            start_at, end_at = "", ""

         edu_detail = {
            "start_at": start_at,
            "end_at": end_at,
            "name": name,
            "description": desc
         }
         if edu_detail not in education_details:
            education_details.append(edu_detail)

   return education_details


@exceptionLog
def getSkills(profile_link: str, driver: Chrome):
   url = profile_link.split("?")[0] + "/details/skills"
   driver.get(url)
   for _ in range(RETRY):
      try:
         main = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'main')))
         break
      except TimeoutException:
         print("[!] Loading took too much time!")
         sleep(1)

   scroll_half(driver)
   scroll_bottom(driver)

   for _ in range(RETRY):
      try:
         main = WebDriverWait(main, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'pvs-list')))
         break
      except TimeoutException:
         print("[!] Loading took too much time!")
         sleep(1)

   skill_details = list()
   try:
      skill = main.find_elements(By.TAG_NAME, "li")
   except NoSuchElementException:
      return skill_details

   for li in skill:
      details = []
      splited = li.text.split("\n")[:12]

      for detail in splited:
         detail = detail.strip()
         if detail and detail not in details and "endors" not in detail.lower():
            details.append(detail)

      if len(details) >= 1:
         skill_details.append(details[0])

   return skill_details


def getProfileDetail(profile_link: str, driver: Chrome, close_driver: bool = False):
   experience_details = getExperiences(profile_link, driver)
   education_details = getEducations(profile_link, driver)
   skills_details = getSkills(profile_link, driver)
   if close_driver:
      driver.close()

   message_log = "[INFO] fetchin profile detail successfuly completed ! | profile_link: %s | length of educations: %s | length of experience: %s" % (profile_link, len(education_details), len(experience_details))
   writeLog(message_log)
   return {
      "profile_link": profile_link,
      "education_details": education_details,
      "experience_details": experience_details,
      "skills_details": skills_details
   }


def completeProfileDetails(is_test: bool = False):
   users = getUncompletedProfiles()
   if is_test:
      users = users[:2]

   driver: Chrome = getDriver()

   for user in users:
      educations = getEducationProfile(user)
      experiences = getExperienceProfile(user)
      if len(educations) == 0 and len(experiences) == 0:
         details = getProfileDetail(user.profile_link, driver)
         educations_detail = details["education_details"]
         experiences_detail = details["experience_details"]

         bulk_edu_data = list()
         bulk_exp_data = list()
         for edu in educations_detail:
            edu["linkedin_user"] = user
            bulk_edu_data.append(Education(**edu))

         for exp in experiences_detail:
            exp["linkedin_user"] = user
            bulk_exp_data.append(Experience(**exp))

         bulkCreateEducation(bulk_edu_data)
         bulkCreateExperience(bulk_exp_data)

      user.is_completed = True
      user.save()

   driver.close()


def exportDetailsAsJson(output: str = "./details.json"):
   data = getProfileDetails()
   print("%s records found" % len(data))
   with open(output, "w") as _file:
      json.dump(data, _file)


def main(keyword: str = KEYWORD, to_json: bool = False):
   valid_users = list()
   driver: Chrome = getDriver()
   driver.minimize_window()
   login(EMAIL, PASSWORD, driver)
   valid_users = search(driver, keyword=keyword)[:MAX_PEOPLE]
   data = []
   for user in valid_users:
      details = getProfileDetail(user["profile_link"], driver)
      if details:
         user["details"] = details

      data.append(user)

   driver.close()
   if to_json:
      store(data, "./output.json")

   insertProfileDetail(data)

