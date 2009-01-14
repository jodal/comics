/* Contributed by Thomas Adamcik <thomas@adamcik.no> 2007-09-30 */

var num_strips = null;
var current;

try {
	current = window.location.toString().split('#')[1].substr(5);
	if (parseInt(current) == NaN) {
		current = -1;
	} else {
		current = parseInt(current);
	}
} catch (error) {
	current = -1;
}


function eventHandler(e) {
	if (num_strips == null) {
		num_strips = document.getElementById('strips').getElementsByTagName('div').length;
	}

	// Ensure that we have an event to work on in all browsers
	if (!e) {
		var e = window.event;
	}

	var code; // Get keycode for event from all browsers
	if (e.keyCode) {
		code = e.keyCode;
	} else if (e.which) {
		code = e.which;
	}

	var handeled = true;
	switch (code) { // Capture hjkl keys
		case 72: // h
			var prev = document.getElementById('prev');
			if (prev) {
				window.location = prev.getAttribute('href');
			}
			break;
		case 74: // j
			if (current < num_strips - 1) {
				current += 1;
				window.location = "#strip" + current;
			}
			break;
		case 75: // k
			if (current < 0) {
				window.location = "#strip0";
				current = 0;
			} else if (current > 0) {
				current -= 1;
				window.location = "#strip" + current;
			}
			break;
		case 76: // l
			var next = document.getElementById('next');
			if (next) window.location = next.getAttribute('href');
			break;
		// Debug key:
		/*
		case 73: // i
			alert("Current: " + current + "\nNum strips: " + num_strips);
			break;
		*/
		default:
			handeled = false;
			break;
	}

	if (handeled) { // Prevent event from bubbleing up if it has been handeled
		e.cancelBubble = true;
		if (e.stopPropagation) {
			e.stopPropagation();
		}
	}
}

// Add event handler to all browsers
document.onkeyup = eventHandler;
if (document.captureEvents) {
	document.captureEvents(Event.KEYUP);
}
