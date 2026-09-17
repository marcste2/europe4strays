/* Click-to-play for YouTube.
   Until the visitor presses play, the page shows a locally hosted thumbnail and
   makes no request to YouTube or Google. The player is only built on click. */
(function () {
  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest(".yt-facade") : null;
    if (!btn) return;
    var id = btn.getAttribute("data-yt") || "";
    if (!/^[\w-]{11}$/.test(id)) return;
    var start = parseInt(btn.getAttribute("data-yt-start") || "0", 10) || 0;

    var frame = document.createElement("iframe");
    frame.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&rel=0" + (start ? "&start=" + start : "");
    frame.title = btn.getAttribute("data-yt-title") || "YouTube video";
    frame.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    frame.setAttribute("allowfullscreen", "");
    btn.parentNode.replaceChild(frame, btn);
    frame.focus();
  });
})();
