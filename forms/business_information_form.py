from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, AnyOf, NumberRange
from datetime import datetime

class BusinessInformationForm(Form):
  business_name = StringField('business_name', validators=[DataRequired()])
  establishment_year = IntegerField('establishment_year', validators=[DataRequired(), NumberRange(min=0, max=datetime.now().year)])
  loan_amount = IntegerField('loan_amount', validators=[DataRequired(), NumberRange(min=1)])
  accounting_software = StringField('accounting_software', validators=[DataRequired(), AnyOf(['xero', 'myob'])])
