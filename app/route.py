from flask import(Flask,render_template, request, redirect, url_for,session,flash)
from app.forms import (VehicleForm,SearchForm)
# from flask_uploads import UploadSet, IMAGES
from werkzeug.utils import secure_filename
from app import app, db
import os
from io import BytesIO
from datetime import datetime
from functools import wraps
from app.models import User, Vehicle
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
            return redirect(url_for('admin_login'))

    return wrapped


@app.route('/', methods=['GET', 'POST'])
@is_logged_in
def home():
    '''
    this will be the route for the landing page after submission. so the form where
    the form where the client will input ID for the vehicle will be rendered here on get and on submission,
    validate from database.
    '''

    form = SearchForm()
    find = User.query.filter_by(username=session['username']).first()
    return render_template('vehicle/search.html', form=form, find=admin)


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
    find = User.query.filter_by(username=session['username']).first()
    result = Vehicle.query.order_by(Vehicle.vehicle_number).all()
    return render_template('index.html', results=result, admin=find.is_admin)


@app.route('/admin/register', methods=['GET', 'POST'])
# @is_logged_in
def admin_signup():
    ''' Admin sign up, where admins are registered '''
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))

    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        is_admin = request.form['is_admin']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        print(is_admin, type(is_admin))
        print(bool(int(is_admin)))

        find = User.query.filter_by(username=username).first()

        if find is not None:
            flash('user already exists', 'danger')
            return redirect(url_for('admin_signup'))

        else:
            save = User(username, lastname, firstname, password_hash, bool(int(is_admin)))
            db.session.add(save)
            db.session.commit()
            flash("successfully registered", "success")
            return redirect(url_for('admin_signup'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    '''
    simple admin for admin and other personnel login
    :return:
    '''

    if request.method == 'POST':
        # get form field
        username = request.form['username']
        password = request.form['password']

        if username and password:
            find = User.query.filter_by(username=username).first()
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

                print(find.is_admin, type(find.is_admin))
                if find.is_admin is True:
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('home'))
        else:
            flash('Invalid input')
            return redirect(url_for('admin_login'))

    return render_template('login.html')

################################################################################################################


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('admin_login'))


@app.route('/admin/vehicle/add', methods=['GET', 'POST'])
@is_logged_in
def add():
     form = VehicleForm()
     if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        vehicle_number = form.vehicle_number.data
        chasis_num = form.chasis_num.data
        color = form.color.data

        '''trying file upload'''
        # img = form.image.data
        # filename = secure_filename(form.image.data.filename)
        # image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # form.image.data.save(image)
        image = 'image'
        existing_vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number).first()

        if existing_vehicle is None:
            vehicle = Vehicle(firstname=firstname,lastname=lastname,vehicle_number=vehicle_number,chasis_num=chasis_num,color=color,image=image)
            db.session.add(vehicle)
            db.session.commit()
            flash('New vehicle added successfully')
            return redirect(url_for('add'))
        else:
            flash('Vehicle already exist')
            return redirect(url_for('add'))

     return render_template('vehicle/register.html', form=form)


@app.route('/vehicle/search', methods=['GET', 'POST'])
@is_logged_in
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
    find1 = User.query.filter_by(username=session['username']).first()
    find = find1.is_admin
    return render_template('vehicle/search.html', form=form, admin=find)


@app.route('/vehicle')
@is_logged_in
def vehicle():
    find = User.query.filter_by(username=session['username']).first()
    result = Vehicle.query.filter_by(vehicle_number=session['search']).first()
    img = '..' + result.image[3:]
    return render_template('vehicle.html',result=result, admin=find.is_admin)


@app.route('/delete/<vehicle_number>', methods=['POST'])
@is_logged_in
def delete(vehicle_number):
    Vehicle.query.filter_by(vehicle_number=vehicle_number).delete()
    db.session.commit()

    flash('This vehicle has been deleted', 'success')
    return redirect(url_for('admin'))
