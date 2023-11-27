import calendar
import random
from datetime import timedelta

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
def get_business_balance_sheet(business_name):
    start_date = datetime.now() - timedelta(days=3 * 365)

    balance_sheet = []

    for _ in range(36):
        profit = random.uniform(-10000, 10000)

        if balance_sheet:
            assets = round(balance_sheet[-1]['assetsValue'] + profit)
        else:
            assets = round(profit)

        balance_sheet.append({
            'year': start_date.year,
            'month': start_date.month,
            'profitOrLoss': round(profit),
            'assetsValue': assets
        })

        # Move to the next month
        start_date += timedelta(days=30)

    return balance_sheet

def get_month_name(month_number):
    month_name = calendar.month_name[month_number]
    return month_name

def evaluate_loan_application(loan_application):
    if random.randint(0, 100) > 50:
        return "approve"
    else:
        return "reject"
