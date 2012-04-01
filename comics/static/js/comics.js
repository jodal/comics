var keyboardNavigation = (function () {
    var getPosition = function ($release) {
        var releasePosition = $release.position().top;
        var navbarHeight = $('.navbar').outerHeight();
        var spacer = 10;
        return releasePosition - navbarHeight - spacer;
    };

    var goToPreviousRelease = function () {
        var $previousRelease = $('.release').filter(function (index) {
            return $(window).scrollTop() > getPosition($(this));
        }).last();

        if ($previousRelease.length) {
            $(window).scrollTop(getPosition($previousRelease));
        } else {
            $(window).scrollTop(0);
        }
    };

    var goToNextRelease = function () {
        var $nextRelease = $('.release').filter(function (index) {
            return $(window).scrollTop() < getPosition($(this));
        }).first();

        if ($nextRelease.length) {
            $(window).scrollTop(getPosition($nextRelease));
        }
    };

    var goToPreviousPage = function () {
        var prev_url = $('#prev').attr('href');
        if (prev_url) {
            window.location = prev_url;
        }
    };

    var goToNextPage = function () {
        var next_url = $('#next').attr('href');
        if (next_url) {
            window.location = next_url;
        }
    };

    return function (event) {
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
})();

$(function() {
    $(document).keypress(keyboardNavigation);
});
