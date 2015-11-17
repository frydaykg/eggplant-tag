import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random	
from google.appengine.api import images
from models import *

class DeleteTag(webapp2.RequestHandler):
	def get(self):
		cur_user = users.get_current_user()	
		if cur_user:
			query = Tag.query(Tag.tag == self.request.query_string)
			if query.iter().has_next():
				tag = query.iter().next()
				tag.key.delete()
			else:
				self.error(404)
		else:
			self.error(401)

app = webapp2.WSGIApplication([
	('/deleteTag', DeleteTag),
], debug=True)
