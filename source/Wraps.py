from functools import wraps
import sys


def prt(func):
    @wraps(func)
    def inner(*args, **kwargs):
        #print(func, args)
        try:
            return func(*args, **kwargs)
        except AttributeError:
            print(sys.exc_info(), func, args)
        except TypeError:
            print(sys.exc_info(), func, args)
        except Exception as e:
            print(sys.exc_info()[0], func, args)
    return inner
