(function () {
  // Highlight the section being read in the left table of contents
  const secs = [...document.querySelectorAll(".sec[id]")];
  const tocLinks = [...document.querySelectorAll(".toc a")];
  const activate = (sec) => {
    tocLinks.forEach((a) => a.classList.toggle("is-active", a.getAttribute("href") === "#" + sec.id));
  };
  if (secs.length && tocLinks.length) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) activate(e.target); });
    }, { rootMargin: "-30% 0px -65% 0px" });
    secs.forEach((s) => obs.observe(s));
    activate(secs[0]);
  }
})();
