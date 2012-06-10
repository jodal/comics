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
        if (event.ctrlKey || event.altKey || event.metaKey) {
            return;
        }
        if ($('#releases').length) {
            if (event.which === 63) { // ?
                event.preventDefault();
                $('.keyboard-shortcuts.modal').modal();
            } else if (event.which === 72 || event.which === 104) { // H or h
                event.preventDefault();
                goToPreviousPage();
            } else if (event.which === 74 || event.which === 106) { // J or j
                event.preventDefault();
                goToNextRelease();
            } else if (event.which === 75 || event.which === 107) { // K or k
                event.preventDefault();
                goToPreviousRelease();
            } else if (event.which === 76 || event.which === 108) { // L or l
                event.preventDefault();
                goToNextPage();
            }
        }
    };
})();

var mycomicsToggler = (function () {
    var showConfirmation = function ($button) {
        $button.css('opacity', 1);
        $button.find('.action').hide();
        $button.find('.confirmation').show();
        $button.addClass('btn-danger');
    };

    var showSuccess = function ($button) {
        $button.css('opacity', 1);
        $button.find('.action').hide();
        $button.find('.confirmation').hide();
        $button.find('.success').show();
        $button
            .removeClass('btn-danger')
            .addClass('btn-success');
    };

    var isMyComicsPage = function () {
        return (window.location + '').match(/\/my\//);
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
                    if (isMyComicsPage()) {
                        var comic = $button.parents('.release').data('comic');
                        $('.release[data-comic="' + comic + '"]')
                            .slideUp('slow')
                            .children().fadeOut('slow');
                    }
                });
            }
        }
    };
})();

var mycomicsEditor = (function () {
    return {
        edit: function (event) {
            event.preventDefault();
            $('#cloud .edit-view').show();
            $('#cloud .show-view').hide();
        },
        cancel: function (event) {
            $('#cloud .show-view').show();
            $('#cloud .edit-view').hide();
        }
    };
})();

var fullSizeToggler = function (event) {
    event.preventDefault();
    if ($('img', this).css('max-width') !== 'none') {
        $('img', this).css('max-width', 'none');
    } else {
        $('img', this).css('max-width', '100%');
    }
};

var newReleaseCheck = (function () {
    var secondsBeforeFirstCheck = 60;

    var getLastReleaseId = function () {
        return $('.release').first().data('release-id');
    };

    var checkForNewReleases = function () {
        var lastReleaseId = getLastReleaseId();
        if (lastReleaseId) {
            $.get('/my/num-releases-since/' + lastReleaseId + '/')
                .done(onSuccess)
                .fail(onFailure);
        }
    };

    var showNewReleaseNotification = function (numReleases) {
        var $el = $('.new-releases-alert');
        $el.find('.new-release-count').html(numReleases);
        $el.slideDown();
    };

    var onSuccess = function (data) {
        if (data.num_releases > 0) {
            showNewReleaseNotification(data.num_releases);
        }
        if (data.seconds_to_next_check !== null) {
            setTimeout(checkForNewReleases, data.seconds_to_next_check * 1000);
        }
    };

    var onFailure = function () {
        setTimeout(checkForNewReleases, secondsBeforeFirstCheck * 1000);
    };

    var isPageOneOfMyComicsLatest = function () {
        return (window.location + '').match(/\/my\/(page1\/)?$/);
    };

    return function () {
        if (isPageOneOfMyComicsLatest()) {
            setTimeout(checkForNewReleases, secondsBeforeFirstCheck * 1000);
        }
    };
})();

$(function () {
    $(document).keypress(keyboardNavigation);
    $('.mycomics-add').click(mycomicsToggler.addComic);
    $('.mycomics-remove').click(mycomicsToggler.removeComic);
    $('.mycomics-edit').click(mycomicsEditor.edit);
    $('.mycomics-cancel').click(mycomicsEditor.cancel);
    $('.release .image a').click(fullSizeToggler);
    newReleaseCheck();
});
