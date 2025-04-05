# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Get database configuration from environment variables
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
db_host = os.environ.get('POSTGRES_HOST')

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://adham:1234@postgres-service/devopsDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Rest of the application code remains the same...

# Define a model for user information
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)
# Automatically create tables (if not already created)
with app.app_context():
    db.create_all()
# Route to display and handle the form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from form
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Create a new user record
        new_user = UserInfo(name=name, email=email, message=message)
        
        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('thank_you'))
        except Exception as e:
            db.session.rollback()
            return f"Error occurred while saving data: {str(e)}"
    
    return render_template('index.html')

# Route to thank the user after form submission
@app.route('/thank-you')
def thank_you():
    return "<h1>Thank you for submitting the form!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
