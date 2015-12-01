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

class TemplateRequest:
	def __init__(self, request):
		self.id = request.key.id()
		self.tag = request.tag.tag
		self.datetime = request.datetime
		self.remoteAddress = request.remoteAddress
		self.country = request.country
		self.region = request.region
		self.city = request.city
		dic = eval(request.headers)
		keys = sorted(dic.keys())
		self.headers = [(x, dic[x]) for x in keys]

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
					templateRequests = sorted([TemplateRequest(x) for x  in requests], key = lambda x: x.datetime)
					tagsWithRequest.append(templateRequests)
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
