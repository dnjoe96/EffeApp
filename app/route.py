from flask import(Flask,render_template, request, redirect, url_for,session,flash)
from app.forms import (VehicleForm,SearchForm)
# from flask_uploads import UploadSet, IMAGES
from werkzeug.utils import secure_filename
from app import app, db
import os
from io import BytesIO
from datetime import datetime
from functools import wraps
from app.models import Personnel, Admin, Vehicle
from werkzeug.security import generate_password_hash, check_password_hash


UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    form = SearchForm()
    return render_template('vehicle/search.html', form=form)


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
    result = Vehicle.query.order_by(Vehicle.vehicle_number).all()
    return render_template('index.html', results=result)


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
            if find:
                verify = check_password_hash(find.password_hash, password)
            else:
                flash('Invalid username or password, try again or visit admin to reset password', 'danger')
                return redirect(url_for('admin_login'))

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


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/admin/vehicle/add', methods=['GET', 'POST'])
def add():
     form = VehicleForm()
     if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        vehicle_number = form.vehicle_number.data
        chasis_num = form.chasis_num.data
        color = form.color.data

        '''trying file upload'''
        img = form.image.data
        # filename = secure_filename(form.image.data.filename)
        # image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # form.image.data.save(image)
        existing_vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()

        if existing_vehicle is None:
            vehicle = Vehicle(firstname=firstname,lastname=lastname,vehicle_number=vehicle_number,chasis_num=chasis_num,color=color,image=img.read())
            db.session.add(vehicle)
            db.session.commit()
            flash('New vehicle added successfully')
            return redirect(url_for('add'))
        else:
            flash('Vehicle already exist')
            return redirect(url_for('add'))

     return render_template('vehicle/register.html', form=form)


@app.route('/vehicle/search', methods=['GET', 'POST'])
def search():
     form = SearchForm()
     if form.validate_on_submit():
        vehicle_number = form.vehicle_number.data
        existing_vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()

        if existing_vehicle is None:
            flash('No such vehicle')
            return redirect(url_for('search'))
        else:
            session['search'] = vehicle_number
            flash('Vehicle exist')
            return redirect(url_for('vehicle'))
        #flash('Vehicle exist')

     return render_template('vehicle/search.html', form=form)


@app.route('/vehicle')
def vehicle():
    result = Vehicle.query.filter_by(vehicle_number=session['search']).first() 
    return render_template('vehicle/vehicle.html',result = result)


@app.route('/delete/<vehicle_number>', methods=['POST'])
def delete(vehicle_number):
    Vehicle.query.filter_by(vehicle_number=vehicle_number).delete()
    db.session.commit()

    flash('This vehicle has been deleted', 'success')
    return redirect(url_for('admin'))
