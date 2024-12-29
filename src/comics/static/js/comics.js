const keyboardNavigation = (() => {
  const getPosition = (element) => {
    const releasePosition = element.offsetTop;
    const navbar = document.querySelector(".navbar");
    const navbarHeight =
      navbar?.style.position === "fixed" ? navbar.offsetHeight : 0;
    const spacer = 10;
    return Math.floor(releasePosition - navbarHeight - spacer);
  };

  const goToPreviousRelease = () => {
    const releases = document.querySelectorAll(".release");
    const scrollTop = window.scrollY;

    const previousRelease = Array.from(releases)
      .reverse()
      .find((release) => scrollTop > getPosition(release) + 1);

    if (previousRelease) {
      window.scrollTo(0, getPosition(previousRelease));
    } else {
      window.scrollTo(0, 0);
    }
  };

  const goToNextRelease = () => {
    const releases = document.querySelectorAll(".release");
    const scrollTop = window.scrollY;

    const nextRelease = Array.from(releases).find(
      (release) => scrollTop < getPosition(release) - 1,
    );

    if (nextRelease) {
      window.scrollTo(0, getPosition(nextRelease));
    }
  };

  const goToPreviousPage = () => {
    const prevLink = document.getElementById("prev");
    if (prevLink?.href) {
      window.location = prevLink.href;
    }
  };

  const goToNextPage = () => {
    const nextLink = document.getElementById("next");
    if (nextLink?.href) {
      window.location = nextLink.href;
    }
  };

  return (event) => {
    if (event.ctrlKey || event.altKey || event.metaKey) {
      return;
    }
    if (!document.getElementById("releases")) {
      return;
    }
    switch (event.key.toLowerCase()) {
      case "?":
        event.preventDefault();
        $(".keyboard-shortcuts.modal").modal();
        break;
      case "h":
        event.preventDefault();
        goToPreviousPage();
        break;
      case "j":
        event.preventDefault();
        goToNextRelease();
        break;
      case "k":
        event.preventDefault();
        goToPreviousRelease();
        break;
      case "l":
        event.preventDefault();
        goToNextPage();
        break;
    }
  };
})();

const mycomicsToggler = (() => {
  const showConfirmation = (button) => {
    button.style.opacity = "1";
    button.querySelector(".action").style.display = "none";
    button.querySelector(".confirmation").style.display = "block";
    button.classList.add("btn-danger");
  };

  const showSuccess = (button) => {
    button.style.opacity = "1";
    button.querySelector(".action").style.display = "none";
    button.querySelector(".confirmation").style.display = "none";
    button.querySelector(".success").style.display = "block";
    button.classList.remove("btn-danger");
    button.classList.add("btn-success");
  };

  const isMyComicsPage = () => String(window.location).match(/\/my\//);

  const serializeForm = (form) => {
    const formData = new FormData(form);
    return new URLSearchParams(formData).toString();
  };

  return {
    addComic: async (event) => {
      event.preventDefault();
      const button = event.currentTarget;
      button.disabled = true;
      const form = button.closest("form");
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "JS-Request": "true",
        },
        body: `${serializeForm(form)}&add_comic=1`,
      });
      if (!response.ok) {
        throw new Error(`Error adding comic: ${response.status}`);
      }
      showSuccess(button);
    },

    removeComic: async (event) => {
      event.preventDefault();
      const button = event.currentTarget;
      if (button.querySelector(".action").offsetParent !== null) {
        // Check if visible
        showConfirmation(button);
      } else {
        button.disabled = true;
        const form = button.closest("form");
        const response = await fetch(form.action, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "JS-Request": "true",
          },
          body: `${serializeForm(form)}&remove_comic=1`,
        });
        if (!response.ok) {
          throw new Error(`Error removing comic: ${response.status}`);
        }
        showSuccess(button);
        if (isMyComicsPage()) {
          const comic = button.closest(".release").dataset.comic;
          const releases = document.querySelectorAll(
            `.release[data-comic="${comic}"]`,
          );
          for (const release of releases) {
            release.style.transition = "all 0.4s";
            release.style.opacity = "0";
            release.style.height = "0";
            release.addEventListener("transitionend", () => release.remove());
          }
        }
      }
    },
  };
})();

const mycomicsEditor = (() => ({
  edit: (event) => {
    event.preventDefault();
    for (const el of document.querySelectorAll(".comics-list .edit-view")) {
      el.classList.remove("hide");
    }
    for (const el of document.querySelectorAll(".comics-list .show-view")) {
      el.classList.add("hide");
    }
  },

  cancel: (event) => {
    for (const el of document.querySelectorAll(".comics-list .show-view")) {
      el.classList.remove("hide");
    }
    for (const el of document.querySelectorAll(".comics-list .edit-view")) {
      el.classList.add("hide");
    }
  },
}))();

const fullSizeToggler = (event) => {
  event.preventDefault();
  const img = event.currentTarget.querySelector("img");
  if (img.style.maxWidth === "none") {
    img.style.maxWidth = "100%";
  } else {
    img.style.maxWidth = "none";
  }
};

const relativify = (timeElement) => {
  const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });
  const date = new Date(timeElement.getAttribute("datetime"));
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
      timeElement.textContent = rtf.format(value, unit);
      return;
    }
  }
};

const newReleaseCheck = (() => {
  const secondsBeforeFirstCheck = 60;

  const getLastReleaseId = () => {
    const firstRelease = document.querySelector(".release");
    return firstRelease?.dataset.releaseId;
  };

  const checkForNewReleases = async () => {
    const lastReleaseId = getLastReleaseId();
    if (lastReleaseId) {
      try {
        const response = await fetch(
          `/my/num-releases-since/${lastReleaseId}/`,
        );
        const data = await response.json();
        onSuccess(data);
      } catch (error) {
        onFailure();
      }
    }
  };

  const showNewReleaseNotification = (numReleases) => {
    const el = document.querySelector(".new-releases-alert");
    const link = el.querySelector("a");
    link.textContent =
      numReleases + (numReleases === 1 ? " new release" : " new releases");
    el.style.transition = "height 0.3s";
    el.style.height = "auto";
    el.style.display = "block";
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
    String(window.location).match(/\/my\/(page1\/)?$/);

  return () => {
    if (isPageOneOfMyComicsLatest()) {
      setTimeout(checkForNewReleases, secondsBeforeFirstCheck * 1000);
    }
  };
})();

document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener("keypress", keyboardNavigation);
  for (const el of document.querySelectorAll(".mycomics-add")) {
    el.addEventListener("click", mycomicsToggler.addComic);
  }
  for (const el of document.querySelectorAll(".mycomics-remove")) {
    el.addEventListener("click", mycomicsToggler.removeComic);
  }
  for (const el of document.querySelectorAll(".mycomics-edit")) {
    el.addEventListener("click", mycomicsEditor.edit);
  }
  for (const el of document.querySelectorAll(".mycomics-cancel")) {
    el.addEventListener("click", mycomicsEditor.cancel);
  }
  for (const el of document.querySelectorAll(".release .image a")) {
    el.addEventListener("click", fullSizeToggler);
  }
  for (const el of document.querySelectorAll(".release time")) {
    relativify(el);
  }
  newReleaseCheck();
});
