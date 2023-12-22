from utils import crawler
import json
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("--crawl", dest="crawl", help="starting to crawl [KEYWORD] from linkedin")
parser.add_argument("--profile-link", dest="profile_link", help="the link of linkedin profile", default="")
parser.add_argument("--to-json", dest="to_json", default="false", help="store collected data in json file")
args = parser.parse_args()

if args.crawl:
   crawler.main(args.crawl)

elif args.single_crawl:
    profile_link = args.profile_link
    if profile_link:
        driver = crawler.getDriver()
        detail = crawler.getProfileDetail(profile_link, driver, close_driver=True)
        if args.to_json and args.to_json != "false":
            with open(args.to_json, "w") as _file:
                json.dump(detail, _file)

elif args.to_json and args.to_json != "false":
   crawler.exportDetailsAsJson(args.to_json)
