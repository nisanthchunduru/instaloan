from datetime import datetime, timedelta
import random

class Base:
  def get_business_balance_sheet(self, business_name):
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
