import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random
from google.appengine.api import users
from models import *
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MyTags(webapp2.RequestHandler):
	def get(self):
		cur_user = users.get_current_user()
		if cur_user:
			tagsWithoutRequest = []
			tagsWithRequest = []
			tagsQuery = Tag.query(Tag.user == cur_user)
			for q in tagsQuery:
				requestQuery = Request.query(Request.tag == q)
				requests = list(requestQuery.iter())
				if requests:
					requests = sorted(requests, key = lambda x: x.datetime)
					tagsWithRequest.append(requests)
				else:
					tagsWithoutRequest.append(q)
			
			template_values = {
            'tagsWithoutRequest': tagsWithoutRequest,
            'tagsWithRequest': tagsWithRequest,
            }
			self.response.write(JINJA_ENVIRONMENT.get_template('templates/header.html').render({'title': 'My tags'}))
			template = JINJA_ENVIRONMENT.get_template('templates/myTags.html')
			self.response.write(template.render(template_values))
			self.response.write(JINJA_ENVIRONMENT.get_template('templates/footer.html').render())
		else:
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/tags/', MyTags),
], debug=True)
