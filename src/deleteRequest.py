import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random	
from google.appengine.api import images
from models import *
import inspect

class DeleteRequest(webapp2.RequestHandler):
	def get(self):
		cur_user = users.get_current_user()	
		if cur_user:
			key = ndb.Key('Request', int(self.request.query_string))
			query = Request.query(ndb.AND(Request.key == key, Request.tag.user == cur_user))
			if query.iter().has_next():
				request = query.iter().next()
				request.key.delete()
			else:
				self.error(404)
		else:
			self.error(401)

app = webapp2.WSGIApplication([
	('/deleteRequest', DeleteRequest),
], debug=True)
