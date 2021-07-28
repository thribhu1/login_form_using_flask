# we can represtent database structe as classes #we call this classes as models
# each class its own table
#sqlite db is a simple dbfile in our database system.
#config values on application
from flask import render_template, url_for, flash, redirect,request
#decrators are using 
import os
import secrets
from PIL import Image
from flask_blog import app,db,bcrypt
from flask_blog.forms import RegistrationForm, LoginForm,UpdateAccountForm
from flask_blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



posts=[{
        'author':'corey_schafer',
        'teaching':'flask',
        'title':'Flask_teachings',
        'len_of_classes':'17'
    },
    {
         'author':'Navin_reddy',
        'teaching':'PYTHON',
        'title':'TELUSKO',
        'len_of_classes':'101'
    }] 
#think it as data_base post

#decorators are just like adding additional functionalities to existing function
#here "/" is nothing but home-page
@app.route("/") # our routes are just like to move between pages using decorator object
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title="about")

@app.route("/register",methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User1=User(username=form.username.data,email=form.email.data,password=hashed_pwd)
        db.session.add(User1)
        db.session.commit()
 
        flash(f'your account has been created! you are able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)



@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login',  form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)#one commonthing pythonist do is throw away the f_name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)

    output_size = (125,125)
    i =Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
    #root_path attribute give the rooth_path of the applicatin 


@app.route("/account",methods=['POST','GET'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('your account has been updatae !', 'success')
        return redirect(url_for('account'))  #(post->get->redirect pattern) #are you sure you want to reload
          #  this is because it will run post request<<< - #  msg comes      your data will be submited are you sure to reload
        #it will relodad post method when we try to submit
    elif request.method == 'GET':  # here we are adding for redirect after the data is updated
        form.username.data="Got you"
        form.email.data=current_user.email

    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file,form=form)