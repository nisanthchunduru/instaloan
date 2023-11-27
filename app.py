from flask import Flask, request, render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
from datetime import datetime, timedelta
import calendar
import os
from helpers import memoize

app = Flask("instaloan")
app.config['SECRET_KEY'] = "dummy_secret_key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://postgres:@localhost/instaloan_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255), nullable=False)
    business_email = db.Column(db.String(255), nullable=False)
    establishment_year = db.Column(db.Integer, nullable=False)
    loan_amount = db.Column(db.Integer, nullable=False)
    accounting_software = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Pending')

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loan_applications/new')
def new_loan_application():
    return render_template('loan_applications/new.html')

@app.route('/login', methods=['POST'])
def create_session():
    business_email = request.form.get('business_email')
    session['business_email'] = business_email
    return redirect(url_for('new_loan_application'))

@app.route('/logout')
def destroy_session():
    if 'business_email' in session:
        session.pop('business_email')
    return redirect(url_for('home'))

@app.route('/loan_applications', methods=['POST'])
def create_loan_application():
    business_name = request.form.get('business_name')
    business_email = session['business_email']
    establishment_year = request.form.get('establishment_year')
    loan_amount = request.form.get('loan_amount')
    accounting_software = request.form.get('accounting_software')

    loan_application = LoanApplication(
        business_name=business_name,
        business_email=business_email,
        establishment_year=establishment_year,
        loan_amount=loan_amount,
        accounting_software=accounting_software,
        status="started"
    )
    db.session.add(loan_application)
    db.session.commit()

    session['current_loan_application_id'] = loan_application.id

    # return redirect(url_for('balance_sheet', loan_application_id=loan_application.id))
    current_year = datetime.now().year
    return redirect(url_for('balance_sheet', loan_application_id=loan_application.id))

def get_month_name(month_number):
    month_name = calendar.month_name[month_number]
    return month_name

@app.route('/loan_applications/<int:loan_application_id>/balance_sheet')
def balance_sheet(loan_application_id):
    loan_application = LoanApplication.query.get_or_404(loan_application_id)

    balance_sheet = get_business_balance_sheet(loan_application.business_name)
    for entry in balance_sheet:
        entry['monthName'] = get_month_name(entry['month'])

    target_year = int(request.args.get('year', datetime.now().year))
    balance_sheet_for_target_year = [entry for entry in balance_sheet if entry['year'] == target_year]
    balance_sheet_years = set(entry['year'] for entry in balance_sheet)
    return render_template(
        'loan_applications/balance_sheet/show.html',
        loan_application_id=loan_application_id,
        balance_sheet_years=balance_sheet_years,
        target_year=target_year,
        balance_sheet_for_target_year=balance_sheet_for_target_year
    )

def evaluate_loan_application(loan_application):
    if random.randint(0, 100) > 50:
        return "approve"
    else:
        return "reject"

    db.session.add(loan_application)
    db.session.commit()

@app.route('/loan_applications/<int:loan_application_id>/balance_sheet/accept')
def accept_balance_sheet(loan_application_id):
    loan_application = LoanApplication.query.get_or_404(loan_application_id)

    loan_application.status = "balance_sheet_accepted"
    db.session.add(loan_application)
    db.session.commit()

    decision = evaluate_loan_application(loan_application)
    if decision == "approve":
        loan_application.status = "approved"
    else:
        loan_application.status = "rejected"
    db.session.add(loan_application)
    db.session.commit()

    if decision == "approve":
        return redirect(url_for('loan_application_approved', loan_application_id=loan_application_id))
    else:
        return redirect(url_for('loan_application_rejected', loan_application_id=loan_application_id))

@app.route('/loan_applications/<int:loan_application_id>/approved')
def loan_application_approved(loan_application_id):
    loan_application = LoanApplication.query.get_or_404(loan_application_id)
    return render_template('loan_applications/approved/show.html')

@app.route('/loan_applications/<int:loan_application_id>/rejected')
def loan_application_rejected(loan_application_id):
    loan_application = LoanApplication.query.get_or_404(loan_application_id)
    return render_template('loan_applications/rejected/show.html')

if __name__ == '__main__':
    is_heroku = 'DYNO' in os.environ
    if is_heroku:
        app.run(host='0.0.0.0')
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)
