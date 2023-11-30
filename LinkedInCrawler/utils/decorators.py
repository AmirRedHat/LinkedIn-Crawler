from log import writeLog



def exceptionLog(func):

   def function(*args, **kwargs):
      try:
         result = func(*args, **kwargs)
         return result
      except Exception as e:
         msg = "[ERROR] in %s function | args: %s | kwargs: %s | error: %s" % (func.__name__, args, kwargs, e)
         writeLog(msg)
         return []

   return function