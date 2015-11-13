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