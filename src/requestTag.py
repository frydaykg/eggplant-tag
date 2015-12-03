import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random	
from google.appengine.api import images
from models import *
from mappers.countryMap import getCountryNameByCode
from mappers.regionMap import getRegionNameByCode

simpleImageData = '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00%\xdbV\xca\x00\x00\x00\x03PLTE\x00\x00\x00\xa7z=\xda\x00\x00\x00\x01tRNS\x00@\xe6\xd8f\x00\x00\x00\nIDAT\x08\xd7c`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82'


class RequestTag(webapp2.RequestHandler):
	def get(self):
		query = Tag.query(Tag.tag == self.request.query_string)
		if query.iter().has_next():
			tag = query.iter().next()
			request = Request()
			request.tag = tag.tag
			request.headers = [Header(key=key, value=self.request.headers[key]) for key in sorted(self.request.headers.keys())]
			request.remoteAddress = str(self.request.remote_addr)
			if 'X-Appengine-Country' in self.request.headers:
			  request.country = getCountryNameByCode(self.request.headers['X-Appengine-Country']).title()
			  if 'X-Appengine-Region' in self.request.headers:
			    request.region = getRegionNameByCode(self.request.headers['X-Appengine-Country'], self.request.headers['X-Appengine-Region']).title()
			if 'X-Appengine-City' in self.request.headers:
			  request.city = str(self.request.headers['X-Appengine-City']).title()
			request.put()

		self.response.write(simpleImageData)
		self.response.headers[ 'Content-Type' ] = 'image/png'
		self.response.headers[ 'Cache-Control' ] = 'no-cache, no-store, must-revalidate'
		self.response.headers[ 'Pragma' ] = 'no-cache'
		self.response.headers[ 'Expires' ] = '0'


app = webapp2.WSGIApplication([
	('/request', RequestTag),
], debug=True)
