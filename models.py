from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy(app)
db = SQLAlchemy()

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255), nullable=False)
    business_email = db.Column(db.String(255), nullable=False)
    establishment_year = db.Column(db.Integer, nullable=False)
    loan_amount = db.Column(db.Integer, nullable=False)
    accounting_software = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')
