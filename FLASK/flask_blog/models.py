from datetime import datetime
from flask_blog import db,login_manager
from flask_login import UserMixin



#You will need to provide a user_loader callback. 
# This callback is used to reload the user object from the user ID stored in the session. 
# It should take the unicode ID of a user, and return the corresponding user object.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User123('{self.username}', '{self.email}', '{self.image_file}')"



    #we wouldnt see this post in db sructr this will be in backround column

    #backref is simlar to adding another column to the user table
    #lazy will load the data in one go.


    #def __repr__(self): #dundermethod this is how our object is printed when our object is printed.
     #   return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

db.create_all()
