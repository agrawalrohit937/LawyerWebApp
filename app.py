from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Simple file-based storage
DATA_FILE = 'data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'appointments': [], 'messages': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/attorneys')
def attorneys():
    return render_template('attorneys.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = load_data()
        message = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'subject': request.form.get('subject'),
            'message': request.form.get('message'),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['messages'].append(message)
        save_data(data)
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        data = load_data()
        appointment = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'service': request.form.get('service'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'message': request.form.get('message'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        data['appointments'].append(appointment)
        save_data(data)
        flash('Your appointment has been scheduled successfully!', 'success')
        return redirect(url_for('appointment'))
    return render_template('appointment.html')

if __name__ == '__main__':
    app.run(debug=True)
