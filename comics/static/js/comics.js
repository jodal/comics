var keyboardNavigation = (function (releases) {
    var index = -1;

    if (!releases) {
        releases = [];
    }

    var scrollToIndex = function () {
        if (index == -1) {
            $(window).scrollTop(0);
        } else {
            var releasePosition = $('#' + releases[index])
                .parent('.release')
                .position().top;
            var navbarHeight = $('.navbar').outerHeight();
            var spacer = 10;
            $(document).scrollTop(releasePosition - navbarHeight - spacer);
        }
    };

    var goToPreviousPage = function() {
        var prev_url = $('#prev').attr('href');
        if (prev_url) {
            window.location = prev_url;
        }
    };

    var goToNextPage = function() {
        var next_url = $('#next').attr('href');
        if (next_url) {
            window.location = next_url;
        }
    };

    var goToPreviousRelease = function() {
        if (index >= 0) {
            index -= 1;
            scrollToIndex();
        }
    };

    var goToNextRelease = function() {
        if (index < releases.length - 1) {
            index += 1;
            scrollToIndex();
        }
    };

    return function(event) {
        if (event.which == 72 || event.which == 104) { // H or h
            event.preventDefault();
            goToPreviousPage();
        } else if (event.which == 74 || event.which == 106) { // J or j
            event.preventDefault();
            goToNextRelease();
        } else if (event.which == 75 || event.which == 107) { // K or k
            event.preventDefault();
            goToPreviousRelease();
        } else if (event.which == 76 || event.which == 108) { // L or l
            event.preventDefault();
            goToNextPage();
        }
    };
})(releases);

$(function() {
    $(document).keypress(keyboardNavigation);
});
