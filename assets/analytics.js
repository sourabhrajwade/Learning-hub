/* Vercel Web Analytics — enable in the Vercel project dashboard */
window.va =
  window.va ||
  function () {
    (window.vaq = window.vaq || []).push(arguments);
  };

(function () {
  var host = window.location.hostname;
  if (host === "localhost" || host === "127.0.0.1") return;
  if (document.querySelector("script[data-vercel-analytics]")) return;

  var script = document.createElement("script");
  script.defer = true;
  script.src = "/_vercel/insights/script.js";
  script.setAttribute("data-vercel-analytics", "true");
  script.onerror = function () {
    script.remove();
  };
  document.head.appendChild(script);
})();
