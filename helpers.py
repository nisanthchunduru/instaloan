import calendar
from accounting_softwares.xero import Xero
from accounting_softwares.myob import Myob

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

@memoize
def get_business_balance_sheet(accounting_software, business_name):
    class_name = accounting_software.title()
    klass = globals()[class_name]
    return klass().get_business_balance_sheet(business_name)

def month_number_to_month_name(month_number):
    month_name = calendar.month_name[month_number]
    return month_name
