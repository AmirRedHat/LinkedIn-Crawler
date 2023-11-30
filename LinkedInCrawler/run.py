from utils import crawler 
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("--crawl", dest="crawl", help="starting to crawl [KEYWORD] from linkedin")
parser.add_argument("--to-json", dest="to_json", default="false", help="store collected data in json file")
args = parser.parse_args()

if args.crawl:
   crawler.main(args.crawl, to_json=to_json)

if args.to_json and args.to_json != "false":
   crawler.exportDetailsAsJson(args.to_json)
