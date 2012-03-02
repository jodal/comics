/* Contributed by Thomas Adamcik <thomas@adamcik.no> 2007-09-30 */

var index = -1;

try {
    releases[0];
} catch (error) {
    var releases = [];
}

try {
    var current = window.location.toString().split('#')[1].split('-')[1];
    if (parseInt(current) == NaN) {
        current = -1;
    } else {
        current = parseInt(current);
    }
    for (var i = 0; i < releases.length; i++) {
        if (current == releases[i].split('-')[1]) {
            index = i;
            break;
        }
    }
} catch (error) {
    index = -1;
}

function eventHandler(e) {
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

    var handled = true;
    switch (code) { // Capture hjkl keys
        case 72: // h
            var prev = document.getElementById('prev');
            if (prev) {
                window.location = prev.getAttribute('href');
            }
            break;
        case 74: // j
            if (index < releases.length - 1) {
                index += 1;
                window.location = '#' + releases[index];
            }
            break;
        case 75: // k
            if (index < 0) {
                index = 0;
                window.location = '#' + releases[index];
            } else if (index > 0) {
                index -= 1;
                window.location = '#' + releases[index];
            }
            break;
        case 76: // l
            var next = document.getElementById('next');
            if (next) window.location = next.getAttribute('href');
            break;
        default:
            handled = false;
            break;
    }

    if (handled) { // Prevent event from bubbleing up if it has been handled
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
