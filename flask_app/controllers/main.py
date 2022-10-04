from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.config import mysqlconnection
from flask import render_template, redirect, session, flash, request
from flask_app.models.users import User
from flask_app.models.categories import Categories
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submitLogin', methods=['POST'])
def login():
    data = {
        "username" : request.form['username'],
        "password" : request.form['password']
    }
    user_db = User.get_by_username(data)
    if not user_db:
        flash("Incorrect Username")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.password, data['password']):
        return redirect('/')
    session['user_id'] = user_db.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    user = User.get_by_id(data)
    categories = Categories.get_categories(data)
    return render_template("dashboard.html" ,user = user, cats = categories)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/submitRegister', methods=['POST'])
def submit_register():
    if not User.validate_register(request.form):
        
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'username' : request.form['username'],
        'password' : pw_hash,
        'email' : request.form['email']
    }
    user = User.submit_register(data)
    session['user_id'] = user
    return redirect('/dashboard')

@app.route('/submitCat', methods=['POST'])
def submit_category():
    data = {
        'id' : session['user_id'],
        'category' : request.form['category']
    }
    Categories.create_category(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_task(id):
    print(id)
    data = {
        'id':id
    }
    Categories.delete_category(data)
    return redirect('/dashboard')