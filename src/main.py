import webapp2
import string
from google.appengine.api import users
from google.appengine.ext import ndb
import random
from google.appengine.api import users
import models

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.write('<html><body>')
			self.response.write('<a href="tags/"> My tags </a>')
			self.response.write('<br><br>')
			
			self.response.write("""
<script src="js/tagManager.js"></script>

<input type="text" class="js-copytextarea" id="tag" value="" size=45 readonly/>
<input type="button" onclick="getTag()" value="Get tag"/>
<input type="button" class="js-textareacopybtn" value="Copy"/>

<script src="js/clipboardCopy.js"></script>
""")
			self.response.write('</body></html>')
		else:
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)