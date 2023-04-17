
# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user import User
import secrets
from flask import request, redirect, url_for


# -- Initialization section --
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
mongo = PyMongo(app)
client = mongo.cx
db = client['schedulify']


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_user(user_id)

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'GET':
        return redirect(url_for('index'))
    email = request.form['email']
    password = request.form['password']
    user = User.check_password(email, password)
    if user:
        login_user(user)
        return redirect(url_for('select'))
    return redirect(url_for('index'))


@app.route('/create-account')
def create_account():
    return render_template('create_account.html')

@app.route('/create-user', methods=['GET','POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_account.html')
    first = request.form['first']
    last = request.form['last']
    email = request.form['email']
    password = request.form['password']

    new_user = User(first, last, email, password=password)
    new_user.save()
    new_user.authenticated = True
    login_user(new_user)

    return redirect(url_for('select'))

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@app.route('/select')
@login_required
def select():
    return render_template('select.html', user=current_user)
