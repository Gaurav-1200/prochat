import os
import time
from flask import Flask, render_template,sessions,redirect,url_for,flash
from wtforms_fields import *
from models import  *
from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user


#Configure app
app =Flask(__name__)
app.secret_key='replace later'

#configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://twfvccgxmrglip:7ac4c07b20f2a6dde7ec808e9373676e8ed841f77d4586a98b04cfc03a7cb56e@ec2-52-72-221-20.compute-1.amazonaws.com:5432/d2iflvdmtg2r94'
app.config['SQL_ALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

#configure Flask Login
login=LoginManager(app)
login.init_app(app)




@login.user_loader
def load_user(id):
    #since id is PRIMARY KEY
    return User.query.get(int(id))



@app.route("/",methods=['GET','POST'])
def index():
  
    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        # HASH of the password
        hashed_pswd = pbkdf2_sha256.hash(password)

        #check duplicate username
        #user_object = User.query.filter_by(username=username).first()
        #if user_object:
            #return "Someone else has taken this user name!!"
        
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registerd Succesfully!! Please Login.', 'success')

        return redirect(url_for('login'))



    return render_template("index.html",form =reg_form)

@app.route("/login",methods=['GET','POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object =User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        if current_user.is_authenticated:
            flash('Please login before accessing the chats!!','danger')
            return redirect(url_for('chat'))


    return render_template("login.html",form=login_form)

@app.route("/chat", methods =['GET','POST'])
#@login_required
def chat():

    if not current_user.is_authenticated:
        flash('Please login to Continue','danger')
        return redirect(url_for('login'))



    return "Chat with me!!"


@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out succesfully.','success')
    return redirect(url_for('login'))


if __name__=="__main__":
    app.run(debug=True)
