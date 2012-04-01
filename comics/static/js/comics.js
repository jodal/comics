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

var usersetToggler = (function () {
    var showConfirmation = function($button) {
        $button.css('opacity', 1);
        $button.find('.action').hide();
        $button.find('.confirmation').show();
        $button.addClass('btn-danger');
    };

    var showSuccess = function($button) {
        $button.css('opacity', 1);
        $button.find('.action').hide();
        $button.find('.confirmation').hide();
        $button.find('.success').show();
        $button
            .removeClass('btn-danger')
            .addClass('btn-success');
    };

    return {
        addComic: function (event) {
            event.preventDefault();
            var $button = $(this);
            $button.attr('disabled', 'disabled');
            var $form = $button.parent('form');
            var data = $form.serialize() + '&add_comic=1';
            $.post($form.attr('action'), data, function () {
                showSuccess($button);
            });
        },
        removeComic: function (event) {
            event.preventDefault();
            var $button = $(this);
            if ($button.find('.action:visible').length) {
                showConfirmation($button);
            } else {
                $button.attr('disabled', 'disabled');
                var $form = $button.parent('form');
                var data = $form.serialize() + '&remove_comic=1';
                $.post($form.attr('action'), data, function () {
                    showSuccess($button);
                    $button
                        .parents('.release').slideUp('slow')
                        .children().fadeOut('slow');
                });
            }
        }
    };
})();

$(function() {
    $(document).keypress(keyboardNavigation);
    $('.userset-add-comic').click(usersetToggler.addComic);
    $('.userset-remove-comic').click(usersetToggler.removeComic);
});
