import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random
from google.appengine.api import users
import models
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.write(JINJA_ENVIRONMENT.get_template('templates/header.html').render({
			'title': 'Welcome',
			'isLogin': True,
			'logoutUrl': users.create_logout_url('/')}))
		else:
			self.response.write(JINJA_ENVIRONMENT.get_template('templates/header.html').render({
			'title': 'Welcome',
			'isLogin': False,
			'loginUrl': users.create_login_url('/')}))
		self.response.write(JINJA_ENVIRONMENT.get_template('templates/main.html').render())
		self.response.write(JINJA_ENVIRONMENT.get_template('templates/footer.html').render())

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
