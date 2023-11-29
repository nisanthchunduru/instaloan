from balance_sheet import BalanceSheet

class PreAssessor:
  def __init__(self, balance_sheet):
    self.balance_sheet = balance_sheet

  def preassess_loan_percentage_for_loan_amount(self, loan_amount):
    balance_sheet = BalanceSheet(self.balance_sheet)
    if balance_sheet.average_assets_value_in_last_12_months > loan_amount:
      return 100
    elif balance_sheet.profit_in_last_12_months > 0:
      return 60
    else:
      return 20
