class BalanceSheet:
  def __init__(self, value):
    self.value = value

  # TODO: Add a more generic method like `profit_since`
  @property
  def profit_in_last_12_months(self):
    profit_in_last_12_months = 0
    for entry in self.balance_sheet[-12:]:
      profit = entry['profitOrLoss']
      profit_in_last_12_months = profit + profit_in_last_12_months

    return profit_in_last_12_months

  # TODO: Add a more generic method like `average_assets_value_since`
  @property
  def average_assets_value_in_last_12_months(self):
    average_assets_value_in_last_12_months = 0
    for entry in self.value[-12:]:
      assets_value = entry['assetsValue']
      average_assets_value_in_last_12_months = average_assets_value_in_last_12_months + assets_value
    average_assets_value_in_last_12_months = average_assets_value_in_last_12_months / 12

    return average_assets_value_in_last_12_months

  @property
  def profit_or_loss_yearly_summary(self):
    summary = {}
    for entry in self.value:
      year = entry['year']
      if not summary[year]:
        summary[year] = 0

      profit_or_loss = entry['profitOrLoss']
      summary[year] += profit_or_loss

    return summary
