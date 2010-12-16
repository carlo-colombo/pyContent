from google.appengine.ext import db

class Repository(db.Model):
    name = db.StringProperty(required=True,name="name")
    


