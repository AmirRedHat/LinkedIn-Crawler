
# Linkedin Crawler
A tool that you can use to find users who are active in your desired field and collect their information.
The information will store in MYSQL and user and (authenticated users and admin users) can access to data through django-restframework API (API documentation is already available in `requirements` directory).
The LinkedIn account cookie will store in cookie.json after the login process is done and after that the crawler engine use exists cookies for verification (Its a legal process).
The authentication system is JWT (JSON WEB TOKEN) that endpoints are available on API documentaion.


# How To Setup
To use the crawler tool you can type "python setup.py" in root path of project (/LinkedinCrawler/).
This command will install python libraries and check crawler dependencies.


# Requirements
- The `chromedriver.exe` must be matched with your chrome browser server (on desktop or server).
- Before start the project you must migrate database (if database or migration folder are not exists):
   1. python manage.py makemigrations
   2. python manage.py migrate


# How to Run
- To starting crawl process just type "python run.py --crawl [your-keyword] --to-json [if-you-want-to-save-as-json]" in your terminal (root directory) and crawler engine will start the process of crawling with config.py and settings.py variables.

- To run django server just type "python manage.py runserver" in your terminal and then server will be reachable on http://localhost:8000 (if you want to deploy it on domain you can use cyberpanel or cpanel tools to config dns).


# Further Details 
- You can change config.py and settings.py variables to setup crawler engine manually.
- You can update cookie.json manually 
- Developers can test modules using test functions using pytest library (/LinkedinCrawler/utils/test/test_crawler.py)
- API Documentation is available on LinkedInCrawler/requirements/LinkedinCrawler.postman_collection.json