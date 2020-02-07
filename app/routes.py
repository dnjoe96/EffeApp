from flask import render_template, request, redirect, url_for
from app import app


@app.routes('/', methods=['GET', 'POST'])
def login():
    '''
    login page will be the route for login, the get request will get the form and render
    html, the post will handle submission
    '''
    pass


@app.routes('/home', methods=['GET', 'POST'])
def home():
    '''
    this will be the route for the landing page after submission. so the form where
    the form where the client will input ID for the vehicle will be rendered here on get and on submission,
    validate from database.
    '''
    pass


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
    This is the route for registeratio of users, it should be on the Nav bar on a side br in the admin panel.
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
    pass


