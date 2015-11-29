import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import users

class Tag(ndb.Model):
	user = ndb.UserProperty(indexed=True)
	tag = ndb.StringProperty(indexed=True)

class Request(ndb.Model):
	tag = ndb.StructuredProperty(Tag)
	datetime = ndb.DateTimeProperty(auto_now_add=True)
	remoteAddress = ndb.StringProperty(indexed=False)
	headers = ndb.StringProperty(indexed=False)
	country = ndb.StringProperty(indexed=False)
