from datetime import datetime


def writeLog(message: str, path: str = "./crawler.log"):
   with open(path, "a") as _file:
      msg = "[%s] %s \n-------------------------------------\n" % (datetime.now(), message)
      _file.write(msg)