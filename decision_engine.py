import random

class DecisionEngine:
  def __init__(self, business_name, establishment_year, yearly_profit_or_loss_summary, preassessed_loan_percentage):
    self.business_name = business_name
    self.establishment_year = establishment_year
    self.yearly_profit_or_loss_summary = yearly_profit_or_loss_summary
    self.preassessed_loan_percentage = preassessed_loan_percentage

  def decision(self):
    if random.uniform(0, 100) > 25:
      return 'approved'
    else:
      return 'rejected'
