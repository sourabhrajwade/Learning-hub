(function () {
  var DEFAULT_CONFIG = {
    storageKey: "learning-hub-fe-progress",
    moduleSlugs: [
      "module-01-foundations",
      "module-02-architecture",
      "module-03-performance",
      "module-04-cdns",
      "module-05-security",
      "module-06-scalability",
      "module-07-case-studies",
      "module-08-interview-playbook",
    ],
  };

  function loadConfig() {
    var el = document.getElementById("course-config");
    if (!el) return DEFAULT_CONFIG;
    try {
      var parsed = JSON.parse(el.textContent);
      if (parsed.storageKey && Array.isArray(parsed.moduleSlugs)) return parsed;
    } catch (e) {}
    return DEFAULT_CONFIG;
  }

  var CONFIG = loadConfig();
  var STORAGE_KEY = CONFIG.storageKey;
  var MODULE_SLUGS = CONFIG.moduleSlugs;
  var TOTAL_MODULES = MODULE_SLUGS.length;

  function getProgress() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return [];
      var parsed = JSON.parse(raw);
      return Array.isArray(parsed)
        ? parsed.filter(function (s) {
            return MODULE_SLUGS.indexOf(s) !== -1;
          })
        : [];
    } catch (e) {
      return [];
    }
  }

  function saveProgress(completed) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(completed));
  }

  function markModuleComplete(slug) {
    if (!slug || MODULE_SLUGS.indexOf(slug) === -1) return;
    var completed = getProgress();
    if (completed.indexOf(slug) === -1) {
      completed.push(slug);
      saveProgress(completed);
    }
  }

  function slugFromPath() {
    var path = window.location.pathname;
    var file = path.split("/").pop() || "";
    if (file.endsWith(".html")) file = file.slice(0, -5);
    if (file === "index") return null;
    return MODULE_SLUGS.indexOf(file) !== -1 ? file : null;
  }

  function progressPercent(completed) {
    return TOTAL_MODULES ? Math.round((completed.length / TOTAL_MODULES) * 100) : 0;
  }

  function ensureClearModal() {
    if (document.getElementById("progress-clear-modal")) return;
    var modal = document.createElement("div");
    modal.id = "progress-clear-modal";
    modal.className = "course-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "progress-clear-title");
    modal.innerHTML =
      '<div class="course-modal-panel">' +
      '<h2 class="course-modal-title" id="progress-clear-title">Clear course progress?</h2>' +
      '<p class="course-modal-text">This will reset all completed modules and set progress back to 0%. This cannot be undone.</p>' +
      '<div class="course-modal-actions">' +
      '<button type="button" class="course-modal-btn" id="progress-clear-cancel">Cancel</button>' +
      '<button type="button" class="course-modal-btn danger" id="progress-clear-confirm">Clear progress</button>' +
      "</div>" +
      "</div>";
    document.body.appendChild(modal);

    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeClearModal();
    });
    document.getElementById("progress-clear-cancel").addEventListener("click", closeClearModal);
    document.getElementById("progress-clear-confirm").addEventListener("click", function () {
      localStorage.removeItem(STORAGE_KEY);
      updateProgressUI();
      closeClearModal();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("open")) closeClearModal();
    });
  }

  function openClearModal() {
    ensureClearModal();
    document.getElementById("progress-clear-modal").classList.add("open");
    document.getElementById("progress-clear-cancel").focus();
  }

  function closeClearModal() {
    var modal = document.getElementById("progress-clear-modal");
    if (modal) modal.classList.remove("open");
  }

  function bindClearButton() {
    var btn = document.getElementById("progress-clear");
    if (!btn || btn.dataset.bound) return;
    btn.dataset.bound = "1";
    btn.addEventListener("click", openClearModal);
  }

  function progressBlockHtml() {
    return (
      '<div class="course-progress-header">' +
      '<span class="course-progress-label">Course Progress</span>' +
      '<span class="course-progress-pct" id="progress-pct">0%</span>' +
      "</div>" +
      '<div class="course-progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="progress-bar">' +
      '<div class="course-progress-fill" id="progress-fill"></div>' +
      "</div>" +
      '<span class="course-progress-meta" id="progress-meta">0 of ' +
      TOTAL_MODULES +
      " modules completed</span>" +
      '<button type="button" class="course-progress-clear" id="progress-clear">Clear progress</button>'
    );
  }

  function injectProgressBar(sidebar) {
    if (!sidebar || document.getElementById("course-progress")) return;
    var nav = sidebar.querySelector(".toc-panel");
    if (!nav) return;
    var wrap = document.createElement("div");
    wrap.className = "course-progress";
    wrap.id = "course-progress";
    wrap.innerHTML = progressBlockHtml();
    nav.parentNode.insertBefore(wrap, nav.nextSibling);
    bindClearButton();
  }

  function updateProgressUI() {
    var completed = getProgress();
    var pct = progressPercent(completed);
    var fill = document.getElementById("progress-fill");
    var pctEl = document.getElementById("progress-pct");
    var meta = document.getElementById("progress-meta");
    var bar = document.getElementById("progress-bar");

    if (fill) fill.style.width = pct + "%";
    if (pctEl) pctEl.textContent = pct + "%";
    if (meta) meta.textContent = completed.length + " of " + TOTAL_MODULES + " modules completed";
    if (bar) bar.setAttribute("aria-valuenow", String(pct));

    document.querySelectorAll(".toc-chapter-link").forEach(function (link) {
      var href = link.getAttribute("href") || "";
      var slug = href.replace(".html", "");
      link.classList.toggle("completed", completed.indexOf(slug) !== -1);
    });

    document.querySelectorAll(".course-index-card").forEach(function (card) {
      var href = card.getAttribute("href") || "";
      var slug = href.replace(".html", "");
      card.classList.toggle("completed", completed.indexOf(slug) !== -1);
    });
  }

  function markCompleteOnScroll(slug) {
    var marked = false;
    function checkScroll() {
      if (marked) return;
      var doc = document.documentElement;
      var scrollTop = window.scrollY || doc.scrollTop;
      var viewport = window.innerHeight;
      var height = doc.scrollHeight;
      if (height <= viewport + 40 || scrollTop + viewport >= height - 120) {
        marked = true;
        markModuleComplete(slug);
        updateProgressUI();
        window.removeEventListener("scroll", checkScroll);
      }
    }
    window.addEventListener("scroll", checkScroll, { passive: true });
    checkScroll();
  }

  var toggle = document.getElementById("toc-toggle");
  var sidebar = document.getElementById("course-sidebar");
  var overlay = document.getElementById("course-overlay");

  if (sidebar) {
    injectProgressBar(sidebar);
    bindClearButton();
    updateProgressUI();

    var currentSlug = slugFromPath();
    if (currentSlug) {
      markCompleteOnScroll(currentSlug);
      document.querySelectorAll(".chapter-nav a.next").forEach(function (btn) {
        btn.addEventListener("click", function () {
          markModuleComplete(currentSlug);
          updateProgressUI();
        });
      });
    }
  }

  if (toggle && sidebar) {
    function closeToc() {
      sidebar.classList.remove("open");
      if (overlay) overlay.classList.remove("open");
    }
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
      if (overlay) overlay.classList.toggle("open");
    });
    if (overlay) overlay.addEventListener("click", closeToc);
  }

  document.querySelectorAll(".toc-sub a, .course-sidebar a[href^='#']").forEach(function (link) {
    link.addEventListener("click", function () {
      if (sidebar) sidebar.classList.remove("open");
      if (overlay) overlay.classList.remove("open");
    });
  });
})();
