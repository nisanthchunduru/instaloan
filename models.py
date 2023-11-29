from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from preassessor import PreAssessor
from accounting_softwares.xero import Xero
from accounting_softwares.myob import Myob
import json
from balance_sheet import BalanceSheet
from decision_engine import DecisionEngine

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
    # preassesssed_loan_percentage = db.Column(db.Integer, nullable=False)
    preassesssed_loan_percentage = db.Column(db.Integer)
    balance_sheet_json = db.Column(JSONB)

    @property
    def balance_sheet(self):
        if not self.balance_sheet_json:
            class_name = self.accounting_software.title()
            klass = globals()[class_name]
            balance_sheet = klass().business_balance_sheet(self.business_name)
            self.balance_sheet_json = json.dumps(balance_sheet)
            db.session.add(self)
            db.session.commit()
            return balance_sheet
        else:
            balance_sheet = json.loads(self.balance_sheet_json)
            return balance_sheet

    # TODO: Add a `Evaluator` class
    def evaluate(self):
        preassessor = PreAssessor(self.balance_sheet)
        self.preassesssed_loan_percentage = preassessor.preassess_loan_percentage_for_loan_amount(self.loan_amount)

        balance_sheet = BalanceSheet(self.balance_sheet)
        decision_engine = DecisionEngine(
            self.business_name,
            self.establishment_year,
            balance_sheet.profit_or_loss_yearly_summary,
            self.preassesssed_loan_percentage
        )
        decision = decision_engine.decision()
        self.status = decision
        db.session.add(self)
        db.session.commit()

        self

    def is_evaluated(self):
        if self.status in ["approved", "rejected"]:
            return True

        return False
