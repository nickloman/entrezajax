from appengine_django.models import BaseModel
from google.appengine.ext import db

class DeveloperRegistration(db.Model):
    contact_name = db.StringProperty(required=True)
    website_url = db.StringProperty(required=True)    
    created_on = db.DateTimeProperty(required=True)

    email = db.StringProperty(required=True)
    tool_id = db.StringProperty(required=True)    
    