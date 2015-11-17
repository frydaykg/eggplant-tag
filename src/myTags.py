import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random
from google.appengine.api import users
from models import *

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
					tagsWithRequest.append(requests)
				else:
					tagsWithoutRequest.append(q)
			self.response.write('<script src="/js/tagManager.js"></script>')
			self.response.write('<script src="/js/clipboardCopy.js"></script>')
			self.response.write('<a href="../"> Main </a>')
			self.response.write('<br>')
			self.response.write('<h1> Not requested yet </h1> <br>')
			for i in tagsWithoutRequest:
				self.response.write('<div id="%s">' % i.tag)
				self.response.write(i.tag)
				self.response.write('&nbsp;&nbsp;<a href="#" onclick="deleteTag(\'%s\')">delete</a>' % i.tag)
				self.response.write('&nbsp;&nbsp;<a href="#" onclick="copyText(window.location.host + \'/request?\' + \'%s\')">copy tag link</a>' % i.tag)
				self.response.write('<br></div>')
			
			self.response.write('<br>')
			self.response.write('<h1> Requested </h1> <br>')
			
			for i in tagsWithRequest:
				self.response.write('<h3>%s</h3	>' % i[0].tag.tag)
				self.response.write('<ul>')
				for j in i:
					headers = eval(j.headers)
					self.response.write('<li>')
					self.response.write('%s <br>' % j.datetime)
					self.response.write('<b>Remote address:</b>&nbsp;%s <br><br>' %  j.remoteAddress)
					for header in headers:
						self.response.write('<b>%s</b>:&nbsp;%s<br>' % (header, headers[header]))
					self.response.write('</li><br>')
				self.response.write('</ul>')
		else:
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/tags/', MyTags),
], debug=True)