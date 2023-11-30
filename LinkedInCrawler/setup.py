import os 
import sys 
import pathlib


ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)))


def checkCrawlerDependencies():
   utils = (ROOT + "/LinkedInCrawler/utils/").replace("\\", "/")
   print(utils)
   config_path = utils + "config.py"
   settings_path = utils + "settings.py"
   if os.path.isdir(utils) and os.path.isfile(config_path) and os.path.isfile(settings_path):
      print("[+] Crawler dependencies are checked !")
      return
   
   raise Exception("[!] Cralwer dependencies faield")


def setup():
   requirements_dir = (ROOT + "/requirements/").replace("\\", "/")
   if not os.path.isdir(requirements_dir):
      raise Exception("[!] requirements directory not found !")

   if os.path.isfile(requirements_dir + "requirements.txt"):
      os.system("pip install -r %s" % requirements_dir + "requirements.txt")
   else:
      raise Exception("[!] requirements.txt not found !")

   checkCrawlerDependencies()


if __name__ == "__main__":
   setup()