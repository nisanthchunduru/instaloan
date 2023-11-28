from flask_sqlalchemy import SQLAlchemy
import random

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

    def evaluate(self):
        if random.randint(0, 100) > 50:
            self.status = "approved"
        else:
            self.status = "rejected"
        db.session.add(self)
        db.session.commit()

    def is_evaluated(self):
        if self.status in ["approved", "rejected"]:
            return True

        return False
