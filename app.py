from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/loan_applications/new')
def new_loan_application():
    return render_template('loan_applications/new.html')

@app.route('/loan_applications/balance_sheet')
def balance_sheet():
    return render_template('loan_applications/balance_sheet/show.html')

@app.route('/loan_applications/approved')
def approved():
    return render_template('loan_applications/approved/show.html')

if __name__ == '__main__':
    app.run(debug=True)
