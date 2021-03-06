from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo
from wtforms import FileField

class SignUpForm(FlaskForm):
    full_name = StringField('Full Name')
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class EditPetForm(FlaskForm):
    name = StringField("Pet's Name", validators=[InputRequired()])
    bio = StringField("Pet's Bio", validators=[InputRequired()])
    submit = SubmitField("Save Changes")

class GetPet(FlaskForm):
    name=StringField("Pet's Name",validators=[InputRequired()])
    bio=StringField("Pet's Bio",validators=[InputRequired()])
    submit=SubmitField("Add Pet")

