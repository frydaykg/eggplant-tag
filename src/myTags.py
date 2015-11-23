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
					templateRequests = [TemplateRequest(x) for x  in requests]
					tagsWithRequest.append(templateRequests)
				else:
					tagsWithoutRequest.append(q)
			
			template_values = {
            'tagsWithoutRequest': tagsWithoutRequest,
            'tagsWithRequest': tagsWithRequest,
            }
			template = JINJA_ENVIRONMENT.get_template('myTags.html')
			self.response.write(template.render(template_values))
		else:
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/tags/', MyTags),
], debug=True)