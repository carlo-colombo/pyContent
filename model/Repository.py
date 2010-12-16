from google.appengine.ext import db

class Repository(db.Model):
    name__ = db.StringProperty(required=True,name="name")
    
    
WEBSITE=Repository(name="website")
