from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#importing flask class
#wsgi aplication # created a server
app = Flask(__name__) #its just the name of the module in the app variable
                      #we are creating instance for the flask class
# jinja2 is the templating system which render dynamic pages by integrating web template and data souces (sql,h5 ,picles)
# WSGI is the web server gateway interface , it serves channel between web server(IIS, apache)
# (it is the which has all the requests)  and web application (callabale web applicaton like API's, )

app.config['SECRET_KEY']='6919919260b060af3eea170504cbc721'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
db=SQLAlchemy(app) #we have a database instance 
bcrypt=Bcrypt(app) #to intialise this bcrypt
login_manager=LoginManager(app)
login_manager.login_view='login'
#The name of the view to redirect to when the user needs to log in. (This can be an absolute URL as well, 
# if your authentication machinery is external to your application.)
login_manager.login_message_category='info'

from flask_blog import routes