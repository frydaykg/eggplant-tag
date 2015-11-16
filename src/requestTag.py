import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random	
from google.appengine.api import images
from models import *

class RequestTag(webapp2.RequestHandler):
	def get(self):
		query = Tag.query(Tag.tag == self.request.query_string)
		if query.iter().has_next():
			tag = query.iter().next()
			request = Request()
			request.tag = tag
			request.headers = str(self.request.headers)
			request.remoteAddress = str(self.request.remote_addr)
			request.put()
		data = "89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52 00 00 00 01 00 00 00 01 01 03 00 00 00 25 DB 56 CA 00 00 00 03 50 4C 54 45 00 00 00 A7 7A 3D DA 00 00 00 01 74 52 4E 53 00 40 E6 D8 66 00 00 00 0A 49 44 41 54 08 D7 63 60 00 00 00 02 00 01 E2 21 BC 33 00 00 00 00 49 45 4E 44 AE 42 60 82"
		data = [int(i,16) for i in data.split(' ')]
		data = ''.join([chr(i) for i in data])
		self.response.write(data)
		self.response.headers[ 'Content-Type' ] = 'image/png'
		self.response.headers[ 'Cache-Control' ] = 'no-cache, no-store, must-revalidate'
		self.response.headers[ 'Pragma' ] = 'no-cache'
		self.response.headers[ 'Expires' ] = '0'

app = webapp2.WSGIApplication([
	('/request', RequestTag),
], debug=True)
