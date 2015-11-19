function copyValueOfElement(elementId, handleFunction) {
  var copyTextarea = document.getElementById(elementId)
  if (copyTextarea) {
  	if (handleFunction)
      copyText(handleFunction(copyTextarea.value));
    else
      copyText(copyTextarea.value)
  }
}

function copyText(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
	  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Copying text command was ' + msg);
    deselectAny();
  } catch (err) {
    console.log('Oops, unable to copy');
  }
  document.body.removeChild(textArea);
}

function deselectAny() {
	if (window.getSelection) {
	  if (window.getSelection().empty) {  // Chrome
	    window.getSelection().empty();
	  } else if (window.getSelection().removeAllRanges) {  // Firefox
	    window.getSelection().removeAllRanges();
	  }
	} else if (document.selection) {  // IE?
	  document.selection.empty();
	}
}