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
			self.response.write('<a href="tags/"> My tags </a>')
			self.response.write('<br><br>')
			
			self.response.write("""<script>
  function getTag() {
    try {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
          document.getElementById("tag").value = xhttp.responseText;
    }
  }
      xhttp.open("GET", "tag/", true);
      xhttp.send();
    }
    catch (E) {
      alert("Oops, something goes wrong. Try again.");
    }
  }
</script>

<input type="text" class="js-copytextarea" id="tag" value="" size=45 readonly/>
<input type="button" onclick="getTag()" value="Get tag"/>
<input type="button" class="js-textareacopybtn" value="Copy"/>

<script>
  var copyTextareaBtn = document.querySelector('.js-textareacopybtn');

	copyTextareaBtn.addEventListener('click', function(event) {
	  var copyTextarea = document.querySelector('.js-copytextarea');
	  copyTextarea.select();

	  try {
	    var successful = document.execCommand('copy');
	    var msg = successful ? 'successful' : 'unsuccessful';
	    console.log('Copying text command was ' + msg);
	  } catch (err) {
	    console.log('Oops, unable to copy');
	  }
	});
</script>
""")
		else:
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)