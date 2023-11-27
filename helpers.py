import calendar

def memoize(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            result = func(*args)
            cache[args] = result
            return result
        else:
            return cache[args]

    return wrapper

def get_month_name(month_number):
    month_name = calendar.month_name[month_number]
    return month_name
