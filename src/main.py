import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random
from google.appengine.api import users
import models

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.write('Hello, %s' % user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)