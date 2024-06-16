from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admissions.db'
db = SQLAlchemy(app)

class AdmissionForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def admission_form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        address = request.form['address']

        new_form = AdmissionForm(name=name, age=age, grade=grade, address=address)
        db.session.add(new_form)
        db.session.commit()

        return redirect(url_for('thank_you'))

    return render_template('admission_form.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/submissions')
def submissions():
    forms = AdmissionForm.query.all()
    return render_template('submissions.html', forms=forms)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
