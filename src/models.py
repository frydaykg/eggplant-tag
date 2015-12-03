import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import users

class Tag(ndb.Model):
	user = ndb.UserProperty(indexed=True)
	tag = ndb.StringProperty(indexed=True)

class Header(ndb.Model):
	key = ndb.StringProperty(indexed=False)
	value = ndb.StringProperty(indexed=False)

class Request(ndb.Model):
	tag = ndb.StringProperty(indexed=True)
	datetime = ndb.DateTimeProperty(auto_now_add=True)
	remoteAddress = ndb.StringProperty(indexed=False)
	headers = ndb.StructuredProperty(Header, indexed=False, repeated=True)
	country = ndb.StringProperty(indexed=False, default='')
	region = ndb.StringProperty(indexed=False, default='')
	city = ndb.StringProperty(indexed=False, default='')
