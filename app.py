from flask import Flask, request, render_template, session, url_for, redirect, abort
from flask_migrate import Migrate
from datetime import datetime
import os
from helpers import get_business_balance_sheet, get_month_name, evaluate_loan_application
from models import db, LoanApplication
from forms.login_form import LoginForm
from forms.business_information_form import BusinessInformationForm

app = Flask("instaloan")
app.config['SECRET_KEY'] = "dummy_secret_key"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://postgres:@localhost/instaloan_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Temporary redirect
def tredirect(url):
    return redirect(url, code=302)

# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
@app.route('/')
def home():
    if 'current_loan_application_id' in session:
        loan_application_id = session['current_loan_application_id']
        return tredirect(url_for('loan_application', id=loan_application_id))

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def create_session():
    login_form = LoginForm(request.form)
    if not login_form.validate():
        return abort(403)

    business_email = request.form.get('business_email')
    session['business_email'] = business_email
    loan_application = LoanApplication.query.filter_by(business_email=business_email).order_by(LoanApplication.id.desc()).first()
    if loan_application:
        session['current_loan_application_id'] = loan_application.id
        if loan_application.is_evaluated():
            return tredirect(url_for('loan_application_decision', loan_application_id=loan_application.id))

    return tredirect(url_for('new_loan_application'))

@app.route('/logout')
def destroy_session():
    if 'business_email' in session:
        session.pop('business_email')
    if 'current_loan_application_id' in session:
        session.pop('current_loan_application_id')
    return tredirect(url_for('home'))

@app.route('/loan_applications/new')
def new_loan_application():
    if 'current_loan_application_id' in session:
        loan_application_id = session['current_loan_application_id']
        return tredirect(url_for('loan_application', id=loan_application_id))

    return render_template('loan_applications/edit.html')

@app.route('/loan_applications/<int:id>')
def loan_application(id):
    loan_application = LoanApplication.query.get_or_404(id)
    return render_template('loan_applications/edit.html', loan_application=loan_application, loan_application_path=("/loan_applications/" + str(id)))

@app.route('/loan_applications', methods=['POST'])
def create_loan_application():
    business_information_form = BusinessInformationForm(request.form)
    if not business_information_form.validate():
        return abort(403)

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

    return tredirect(url_for('balance_sheet', loan_application_id=loan_application.id))

@app.route('/loan_applications/<int:loan_application_id>', methods=['POST', 'PUT'])
def update_loan_application(loan_application_id):
    loan_application = LoanApplication.query.get_or_404(loan_application_id)
    if loan_application.is_evaluated():
        return tredirect(url_for('balance_sheet', loan_application_id=loan_application.id))

    business_information_form = BusinessInformationForm(request.form)
    if not business_information_form.validate():
        return abort(403)

    if not loan_application.status == "started":
        return abort(403)

    if loan_application.is_evaluated() is False:
        loan_application.business_name = request.form.get('business_name')
        loan_application.establishment_year = request.form.get('establishment_year')
        loan_application.loan_amount = request.form.get('loan_amount')
        loan_application.accounting_software = request.form.get('accounting_software')
        db.session.add(loan_application)
        db.session.commit()

    return tredirect(url_for('balance_sheet', loan_application_id=loan_application.id))

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

@app.route('/loan_applications/<int:loan_application_id>/balance_sheet/accept')
def accept_balance_sheet(loan_application_id):
    loan_application = LoanApplication.query.get_or_404(loan_application_id)
    if loan_application.is_evaluated():
        return tredirect(url_for('loan_application_decision', loan_application_id=loan_application.id))

    loan_application = LoanApplication.query.get_or_404(loan_application_id)
    if not loan_application.status == "started":
        return abort(403)

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

    return tredirect(url_for('loan_application_decision', loan_application_id=loan_application.id))

@app.route('/loan_applications/<int:loan_application_id>/decision')
def loan_application_decision(loan_application_id):
    loan_application = LoanApplication.query.get_or_404(loan_application_id)
    if not loan_application.is_evaluated():
        return abort(403)

    return render_template('loan_applications/decision/show.html', loan_application=loan_application)

if __name__ == '__main__':
    is_heroku = 'DYNO' in os.environ
    if is_heroku:
        app.run(host='0.0.0.0')
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)
