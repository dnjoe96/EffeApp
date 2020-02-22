from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from functools import wraps
from app.models import Personnel, Admin, Car_Registration
from werkzeug.security import generate_password_hash, check_password_hash


def is_logged_in(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized access, Please login', 'danger')
            return redirect(url_for('login'))

    return wrapped


@app.routes('/', methods=['GET', 'POST'])
def login():
    '''
    login page will be the route for login, the get request will get the form and render
    html, the post will handle submission
    '''

    if request.method == 'POST':
        # get form field
        username = request.form['username']
        password = request.form['password']

        if username and password:
            find = Personnel.Query.filter_by(username=username).one()
            verify = check_password_hash(find.password_hash, password)

            if verify:
                flash('successfully logged in', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password, try again or visit admin to reset password', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid input')
            return redirect(url_for('login'))

    return render_template('index.html')


@app.routes('/home', methods=['GET', 'POST'])
def home():
    '''
    this will be the route for the landing page after submission. so the form where
    the form where the client will input ID for the vehicle will be rendered here on get and on submission,
    validate from database.
    '''
    pass


@app.route('/admin/sign_up')
def admin_sign_up():
    ''' Admin sign up, where admins are registered '''

    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        find = Personnel.Query.filter_by(username=username)

        if not find:
            save = Admin(username, lastname, firstname, password_hash)
            db.session.add(save)
            db.session.commit()
            flash("successfully registered", "success")
            return redirect(url_for('main'))

        else:
            flash('user already exists')
            return redirect(url_for('presonnel_register'))

    return render_template('personnel_register.html')



@app.routes('/admin')
def admin():
    '''
    This renders the admin landing page. admin page will query everything from the database which will contain all the information of registered
    vehicles.
    '''
    pass


@app.routes('/admin/register', methods=['GET', 'POST'])
def vehicle_register():
    '''
    This is the route for registration of users, it should be on the Nav bar on a side br in the admin panel.
    on get, it renders the data entry form, on post, it submits to the database
    :return:
    '''
    pass


@app.routes('/admin/login', methods=['GET', 'POST'])
def admin_login():
    '''
    simple admin login
    :return:
    '''
    pass


@app.routes('/admin/personnel', methods=['GET', 'POST'])
def personnel_register():
    '''
    This is the route for registeratio of users, it should be on the Nav bar on a side br in the admin panel.
    on get, it renders the data entry form, on post, it submits to the database
    :return:
    '''

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        find = Personnel.Query.filter_by(username=username)

        if not find:
            save = Personnel(username, password_hash)  # sender ID will be passed in here when i obtain it
            db.session.add(save)
            db.session.commit()
            flash("successfully registered", "success")
            return redirect(url_for('main'))

        else:
            flash('user already exists')
            return redirect(url_for('presonnel_register'))

    return render_template('personnel_register.html')


