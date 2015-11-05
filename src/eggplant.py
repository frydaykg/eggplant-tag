import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random
from google.appengine.api import users

class Tag(ndb.Model):
	user = ndb.UserProperty(indexed=True)
	tag = ndb.StringProperty(indexed=True)

class Request(ndb.Model):
	tag = ndb.StructuredProperty(Tag)
	datetime = ndb.DateTimeProperty(auto_now_add=True)
	requestData = ndb.StringProperty(indexed=False)


class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.write('Hello, %s' % user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))

class TagGenerator(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			tag = Tag()
			tag.user = user
			tag.tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
			tag.put()
			self.response.write('Successfully generated. Tag is %s' % tag.tag)
		else:
			self.redirect(users.create_login_url(self.request.uri))

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
			
			self.response.write('<h1> Not requested yet </h1> <br>')
			for i in tagsWithoutRequest:
				self.response.write('%s <br>' % i.tag)
			
			self.response.write('<br>')
			self.response.write('<h1> Requested </h1> <br>')
			
			for i in tagsWithRequest:
				self.response.write('<h3>%s</h3	>' % i[0].tag.tag)
				self.response.write('<ul>')
				for j in i:
					self.response.write('<li>%s <br> %s</li>' % (j.datetime, j.requestData.replace('\n', '<br>')))
				self.response.write('</ul>')
				

		else:
			self.redirect(users.create_login_url(self.request.uri))

class RequestTag(webapp2.RequestHandler):
	def get(self):
		query = Tag.query(Tag.tag == self.request.query_string)
		if query.iter().has_next():
			tag = query.iter().next()
			request = Request()
			request.tag = tag
			request.requestData = self.getBody()
			request.put()
		self.response.headers['Content-Type'] = 'image/png'
			
	def getBody(self):
		argumentData = ""
		for i in self.request.arguments():
			argumentData += i + ": " + str(self.request.get_all(i)) + '\n'
		data = """Remote Address: %s

Full URL: %s

Headers: %s

Cookies: %s

Arguments:
%s""" % (str(self.request.remote_addr), str(self.request.url), str(self.request.headers), str(self.request.cookies), argumentData)
		return data


app = webapp2.WSGIApplication([
	('/', MainPage),
	('/tag', TagGenerator),
	('/tags', MyTags),
	('/request', RequestTag),
], debug=True)