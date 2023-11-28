from wtforms import Form, EmailField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
   business_email = EmailField('business_email', [DataRequired(), Email()])
