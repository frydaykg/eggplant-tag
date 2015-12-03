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
			query = Request.query(Request.key == key)			
			if query.iter().has_next():
				request = query.iter().next()
				queryTags = Tag.query(ndb.AND(Tag.tag == request.tag, Tag.user == cur_user))
				if queryTags.iter().has_next():
					request.key.delete()
			else:
				self.error(404)
		else:
			self.error(401)

app = webapp2.WSGIApplication([
	('/deleteRequest', DeleteRequest),
], debug=True)
