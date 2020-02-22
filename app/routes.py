from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from functools import wraps
from app.models import Personnel, Admin
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



@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    this will be the route for the landing page after submission. so the form where
    the form where the client will input ID for the vehicle will be rendered here on get and on submission,
    validate from database.
    '''
    return render_template('index.html')


####################################################################################################################
############################### ADMIN SECTION ######################################################################
####################################################################################################################

@app.route('/admin')
@is_logged_in
def admin():
    '''
    This renders the admin landing page. admin page will query everything from the database which will contain all the information of registered
    vehicles.
    '''
    return render_template('admin/dashboard.html')


@app.route('/admin/sign_up', methods=['GET', 'POST'])
def admin_signup():
    ''' Admin sign up, where admins are registered '''
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))

    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        find = Admin.query.filter_by(username=username).first()

        if find is not None:
            flash('user already exists', 'danger')
            return redirect(url_for('admin_signup'))

        else:
            save = Admin(username, lastname, firstname, password_hash)
            db.session.add(save)
            db.session.commit()
            flash("successfully registered", "success")
            return redirect(url_for('admin_login'))

    return render_template('register.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    '''
    simple admin login
    :return:
    '''

    if request.method == 'POST':
        # get form field
        username = request.form['username']
        password = request.form['password']

        if username and password:
            find = Admin.query.filter_by(username=username).first()
            verify = check_password_hash(find.password_hash, password)

            if find is None or verify is False:
                flash('Invalid username or password, try again or visit admin to reset password', 'danger')
                return redirect(url_for('admin_login'))

            else:
                session['logged_in'] = True
                session['username'] = username
                flash('successfully logged in', 'success')
                return redirect(url_for('admin'))
        else:
            flash('Invalid input')
            return redirect(url_for('admin_login'))

    return render_template('login.html')

################################################################################################################


################################################################################################################
################## PERSONNEL REGISTRATION BY AN ADMIN AND PERSONNEL LOGIN ######################################
################################################################################################################

@app.route('/admin/personnel', methods=['GET', 'POST'])
@is_logged_in
def personnel_register():
    '''
    This is the route for registeratio of users, it should be on the Nav bar on a side br in the admin panel.
    on get, it renders the data entry form, on post, it submits to the database
    :return:
    '''

    if request.method == "POST":
        username = request.form['username']
        password = 'password' # here is the default password
        password_hash = generate_password_hash(password)

        find = Personnel.query.filter_by(username=username).first()

        if find is not None:
            save = Personnel(username, password_hash)  # sender ID will be passed in here when i obtain it
            db.session.add(save)
            db.session.commit()
            flash("successfully registered", "success")
            return redirect(url_for('personnel_register'))

        else:
            flash('user already exists')
            return redirect(url_for('presonnel_register'))

    return render_template('register_personnel.html')


@app.route('/login', methods=['GET', 'POST'])
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
            find = Personnel.query.filter_by(username=username).first()
            verify = check_password_hash(find.password_hash, password)

            if find is not None or verify is True:
                session['logged_in'] = True
                session['username'] = username
                flash('successfully logged in', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password, try again or visit admin to reset password', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Invalid input')
            return redirect(url_for('login'))

    return render_template('login.html')

#############################################################################################################


#############################################################################################################
########################### VEHICLE REGISTRATION ############################################################
#############################################################################################################

@app.route('/admin/register', methods=['GET', 'POST'])
def vehicle_register():
    '''
    This is the route for registration of users, it should be on the Nav bar on a side br in the admin panel.
    on get, it renders the data entry form, on post, it submits to the database
    :return:
    '''
    pass
