const keyboardNavigation = (() => {
  const getPosition = ($release) => {
    const releasePosition = $release.position().top;
    let navbarHeight = 0;
    if ($(".navbar").css("position") === "fixed") {
      navbarHeight = $(".navbar").outerHeight();
    }
    const spacer = 10;
    return Math.floor(releasePosition - navbarHeight - spacer);
  };

  const goToPreviousRelease = () => {
    const $previousRelease = $(".release")
      .filter(function (index) {
        return $(window).scrollTop() > getPosition($(this)) + 1;
      })
      .last();

    if ($previousRelease.length) {
      $(window).scrollTop(getPosition($previousRelease));
    } else {
      $(window).scrollTop(0);
    }
  };

  const goToNextRelease = () => {
    const $nextRelease = $(".release")
      .filter(function (index) {
        return $(window).scrollTop() < getPosition($(this)) - 1;
      })
      .first();

    if ($nextRelease.length) {
      $(window).scrollTop(getPosition($nextRelease));
    }
  };

  const goToPreviousPage = () => {
    const prev_url = $("#prev").attr("href");
    if (prev_url) {
      window.location = prev_url;
    }
  };

  const goToNextPage = () => {
    const next_url = $("#next").attr("href");
    if (next_url) {
      window.location = next_url;
    }
  };

  return (event) => {
    if (event.ctrlKey || event.altKey || event.metaKey) {
      return;
    }
    if ($("#releases").length) {
      if (event.which === 63) {
        // ?
        event.preventDefault();
        $(".keyboard-shortcuts.modal").modal();
      } else if (event.which === 72 || event.which === 104) {
        // H or h
        event.preventDefault();
        goToPreviousPage();
      } else if (event.which === 74 || event.which === 106) {
        // J or j
        event.preventDefault();
        goToNextRelease();
      } else if (event.which === 75 || event.which === 107) {
        // K or k
        event.preventDefault();
        goToPreviousRelease();
      } else if (event.which === 76 || event.which === 108) {
        // L or l
        event.preventDefault();
        goToNextPage();
      }
    }
  };
})();

const mycomicsToggler = (() => {
  const showConfirmation = ($button) => {
    $button.css("opacity", 1);
    $button.find(".action").hide();
    $button.find(".confirmation").show();
    $button.addClass("btn-danger");
  };

  const showSuccess = ($button) => {
    $button.css("opacity", 1);
    $button.find(".action").hide();
    $button.find(".confirmation").hide();
    $button.find(".success").show();
    $button.removeClass("btn-danger").addClass("btn-success");
  };

  const isMyComicsPage = () => `${window.location}`.match(/\/my\//);

  return {
    addComic: function (event) {
      event.preventDefault();
      const $button = $(this);
      $button.attr("disabled", "disabled");
      const $form = $button.parent("form");
      const data = `${$form.serialize()}&add_comic=1`;
      $.post($form.attr("action"), data, () => {
        showSuccess($button);
      });
    },
    removeComic: function (event) {
      event.preventDefault();
      const $button = $(this);
      if ($button.find(".action:visible").length) {
        showConfirmation($button);
      } else {
        $button.attr("disabled", "disabled");
        const $form = $button.parent("form");
        const data = `${$form.serialize()}&remove_comic=1`;
        $.post($form.attr("action"), data, () => {
          showSuccess($button);
          if (isMyComicsPage()) {
            const comic = $button.parents(".release").data("comic");
            $(`.release[data-comic="${comic}"]`)
              .slideUp("slow")
              .children()
              .fadeOut("slow");
          }
        });
      }
    },
  };
})();

const mycomicsEditor = (() => ({
  edit: (event) => {
    event.preventDefault();
    $(".comics-list .edit-view").removeClass("hide");
    $(".comics-list .show-view").addClass("hide");
  },
  cancel: (event) => {
    $(".comics-list .show-view").removeClass("hide");
    $(".comics-list .edit-view").addClass("hide");
  },
}))();

const fullSizeToggler = function (event) {
  event.preventDefault();
  if ($("img", this).css("max-width") !== "none") {
    $("img", this).css("max-width", "none");
  } else {
    $("img", this).css("max-width", "100%");
  }
};

$.fn.relativify = function () {
  const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
  return this.each(function () {
    const date = new Date($(this).attr("datetime"));
    const now = new Date();
    const diffInSeconds = (date - now) / 1000;
    const intervals = {
      year: 86400 * 365,
      month: 86400 * 30,
      week: 86400 * 7,
      day: 86400,
      hour: 3600,
      minute: 60,
      second: 1,
    };
    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
      const value = Math.round(diffInSeconds / secondsInUnit);
      if (Math.abs(value) >= 1) {
        $(this).text(rtf.format(value, unit));
        return;
      }
    }
  });
};

const newReleaseCheck = (() => {
  const secondsBeforeFirstCheck = 60;

  const getLastReleaseId = () => $(".release").first().data("release-id");

  const checkForNewReleases = () => {
    const lastReleaseId = getLastReleaseId();
    if (lastReleaseId) {
      $.get(`/my/num-releases-since/${lastReleaseId}/`)
        .done(onSuccess)
        .fail(onFailure);
    }
  };

  const showNewReleaseNotification = (numReleases) => {
    const $el = $(".new-releases-alert");
    $el
      .find("a")
      .text(
        numReleases + (numReleases === 1 ? " new release" : " new releases"),
      );
    $el.slideDown();
  };

  const onSuccess = (data) => {
    if (data.num_releases > 0) {
      showNewReleaseNotification(data.num_releases);
    }
    if (data.seconds_to_next_check !== null) {
      setTimeout(checkForNewReleases, data.seconds_to_next_check * 1000);
    }
  };

  const onFailure = () => {
    setTimeout(checkForNewReleases, secondsBeforeFirstCheck * 1000);
  };

  const isPageOneOfMyComicsLatest = () =>
    `${window.location}`.match(/\/my\/(page1\/)?$/);

  return () => {
    if (isPageOneOfMyComicsLatest()) {
      setTimeout(checkForNewReleases, secondsBeforeFirstCheck * 1000);
    }
  };
})();

$(() => {
  $(document).keypress(keyboardNavigation);
  $(".mycomics-add").click(mycomicsToggler.addComic);
  $(".mycomics-remove").click(mycomicsToggler.removeComic);
  $(".mycomics-edit").click(mycomicsEditor.edit);
  $(".mycomics-cancel").click(mycomicsEditor.cancel);
  $(".release .image a").click(fullSizeToggler);
  $(".release time").relativify();
  newReleaseCheck();
});
