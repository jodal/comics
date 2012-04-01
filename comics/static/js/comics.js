var keyboardNavigation = (function () {
    var getTopPosition = function ($release) {
        var releasePosition = $release.position().top;
        var navbarHeight = $('.navbar').outerHeight();
        var spacer = 10;
        return releasePosition - navbarHeight - spacer;
    };

    var getBottomPosition = function ($release) {
        return getTopPosition($release) + $release.outerHeight();
    };

    var scrollTo = function (target) {
        var position;
        if (target === 'top') {
            position = 0;
        } else {
            position = getTopPosition(target);
        }
        $(window).scrollTop(position);
    };

    var goToPreviousRelease = function () {
        var $previousRelease = $('.release').filter(function (index) {
            return $(window).scrollTop() > getTopPosition($(this));
        }).last();

        if ($previousRelease.length) {
            scrollTo($previousRelease);
        } else {
            scrollTo('top');
        }
    };

    var goToNextRelease = function () {
        var $firstRelease = $('.release').first();
        var beforeFirstRelease = (
            $(window).scrollTop() < getTopPosition($firstRelease));
        if (beforeFirstRelease) {
            return scrollTo($firstRelease);
        }

        var $nextRelease = $('.release').filter(function (index) {
            return $(window).scrollTop() < getBottomPosition($(this));
        }).first().next();

        if ($nextRelease.length) {
            scrollTo($nextRelease);
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
