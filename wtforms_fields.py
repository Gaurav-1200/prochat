from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length,EqualTo,ValidationError
from models import User

from passlib.hash import pbkdf2_sha256

def invalid_credentials(form,field):
        """Username and password checker"""

        username_entered = form.username.data
        password_enetered = field.data

        user_object= User.query.filter_by(username=username_entered).first()
        if user_object is None:
                raise ValidationError("Username or Password is incorrect")
       # elif password_enetered != user_object.password:
        elif not pbkdf2_sha256.verify(password_enetered,user_object.password):
                raise ValidationError("Username or Password is incorrect")







class RegistrationForm(FlaskForm):
    """Registration Form"""

    username = StringField('username_label',
            validators=[InputRequired(message="Username Required"),Length(min=4,max=25, message="Username must be b/w 4 and 25 charcters")])
    password =PasswordField('password_field',
            validators=[InputRequired(message="Password Required"),Length(min=4,max=25, message="Password must be b/w 4 and 25 charcters")])
    confirm_pswd= PasswordField('comfirm_pswd_label',
                validators=[InputRequired(message="Username Required"),EqualTo('password',message="Password must match")])
    submit_button = SubmitField('Create')


    def validate_username(self, username):
            user_object =User.query.filter_by(username=username.data).first()
            if user_object:
                    raise ValidationError("Username already exists! Select a different username. ")

class LoginForm(FlaskForm):
        """Login form"""

        username = StringField('username_label',validators=[InputRequired(message="Username required")])
        password = PasswordField('password_label',validators=[InputRequired(message="Password Required"),invalid_credentials])
        submit_button = SubmitField('Login')
