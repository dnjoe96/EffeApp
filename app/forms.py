from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField,SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed



class VehicleForm(FlaskForm):
    firstname = StringField(u'First Name', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    lastname = StringField(u'Last Name', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    vehicle_number= StringField(u'Vehicle Number', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    chasis_num= StringField(u'Chasis Number', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    color= StringField(u'Vehicle Color', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    image = FileField('Image')
    submit = SubmitField('submit')

class SearchForm(FlaskForm):
    vehicle_number= StringField(u'Enter Vehicle Number', validators=[validators.input_required(),validators.Length(min=3, max=50)])
    submit = SubmitField('verify')