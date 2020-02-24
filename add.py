from flask import(render_template, redirect, url_for,session,flash)
from app.forms import (VehicleForm,SearchForm)
from werkzeug.utils import secure_filename
from app import app, db
import os
from app.models import Vehicle


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/vehicle/add', methods=['GET', 'POST'])
def add():
     form = VehicleForm()
     if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        vehicle_number = form.vehicle_number.data
        chasis_num = form.chasis_num.data
        color = form.color.data
        filename = secure_filename(form.image.data.filename)
        image = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.image.data.save(image)
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


@app.route('/admin/vehicle/search', methods=['GET', 'POST'])
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