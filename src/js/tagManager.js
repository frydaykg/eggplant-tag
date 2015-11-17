function getTag() {
	try {
	  var xhttp = new XMLHttpRequest();
	  xhttp.onreadystatechange = function() {
	    if (xhttp.readyState == 4 && xhttp.status == 200) {
	      document.getElementById("tag").value = xhttp.responseText;
	}
	  }
	  xhttp.open("GET", "/tag/", true);
	  xhttp.send();
	}
	catch (E) {
	  alert("Oops, something goes wrong. Try again.");
	}
};

function deleteTag(tag) {
	try {
	  var xhttp = new XMLHttpRequest();
	  xhttp.open("GET", "/deleteTag?" + tag, true);
	  xhttp.onreadystatechange = function() {
		  if (xhttp.readyState == 4 && xhttp.status == 200) {
		      document.getElementById(tag).style.display = 'none';
		  }
      }
	  xhttp.send();
	}
	catch (E) {
	  alert("Oops, something goes wrong. Try again.");
	}
};