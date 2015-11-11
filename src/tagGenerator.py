import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random
from google.appengine.api import users
from models import *

class TagGenerator(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			tag = Tag()
			tag.user = user
			tag.tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
			tag.put()
			self.response.write(tag.tag)
		else:
			self.error(401)


app = webapp2.WSGIApplication([
	('/tag/', TagGenerator),
], debug=True)