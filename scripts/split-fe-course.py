#!/usr/bin/env python3
"""Split frontend-system-design-course.html into chapter pages."""

from pathlib import Path
import re
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "frontend-system-design-course.html"
OUT = ROOT / "frontend-system-design"
COURSE_PREFIX = "/frontend-system-design"

CHAPTERS = [
    {
        "slug": "module-01-foundations",
        "section_id": "module-1",
        "num": 1,
        "title": "Foundations",
        "subtitle": "Browser fundamentals, the RADIO framework, HTTP, and the rendering pipeline.",
        "badge": "Beginner",
        "subsections": [
            ("m1-intro", "1.1 What is Frontend System Design?"),
            ("m1-process", "1.2 The RADIO Framework"),
            ("m1-network", "1.3 Browser, HTTP, Networking"),
            ("m1-render", "1.4 Rendering Pipeline"),
        ],
    },
    {
        "slug": "module-02-architecture",
        "section_id": "module-2",
        "num": 2,
        "title": "Architecture",
        "subtitle": "CSR, SSR, SSG, SPA patterns, state management, and component design.",
        "badge": "Intermediate",
        "subsections": [
            ("m2-rendering-strategies", "2.1 CSR / SSR / SSG / ISR"),
            ("m2-spa", "2.2 SPA Architecture (React)"),
            ("m2-state", "2.3 State Management Patterns"),
            ("m2-data", "2.4 Data Fetching & Caching"),
            ("m2-component", "2.5 Component Design"),
        ],
    },
    {
        "slug": "module-03-performance",
        "section_id": "module-3",
        "num": 3,
        "title": "Performance",
        "subtitle": "Core Web Vitals, bundling, assets, runtime optimization, and virtualization.",
        "badge": "Intermediate",
        "subsections": [
            ("m3-cwv", "3.1 Core Web Vitals"),
            ("m3-bundle", "3.2 Bundling & Code Splitting"),
            ("m3-images", "3.3 Images, Fonts, Assets"),
            ("m3-runtime", "3.4 Runtime Optimization"),
            ("m3-virt", "3.5 Virtualization & Lists"),
        ],
    },
    {
        "slug": "module-04-cdns",
        "section_id": "module-4",
        "num": 4,
        "title": "CDNs",
        "subtitle": "Cache hierarchies, invalidation strategies, and edge computing.",
        "badge": "Advanced",
        "subsections": [
            ("m4-what", "4.1 What & Why"),
            ("m4-cache", "4.2 Cache Hierarchies"),
            ("m4-invalid", "4.3 Invalidation Strategies"),
            ("m4-edge", "4.4 Edge Computing"),
        ],
    },
    {
        "slug": "module-05-security",
        "section_id": "module-5",
        "num": 5,
        "title": "Security",
        "subtitle": "XSS, CSRF, CORS, auth patterns, CSP, and supply chain risks.",
        "badge": "Advanced",
        "subsections": [
            ("m5-xss", "5.1 XSS"),
            ("m5-csrf", "5.2 CSRF"),
            ("m5-cors", "5.3 CORS & SOP"),
            ("m5-auth", "5.4 Auth (Cookies vs JWT)"),
            ("m5-csp", "5.5 CSP, SRI, Headers"),
            ("m5-supply", "5.6 Supply Chain"),
        ],
    },
    {
        "slug": "module-06-scalability",
        "section_id": "module-6",
        "num": 6,
        "title": "Scalability",
        "subtitle": "Monorepos, design systems, micro-frontends, i18n, and observability.",
        "badge": "Advanced",
        "subsections": [
            ("m6-monorepo", "6.1 Monorepos"),
            ("m6-ds", "6.2 Design Systems"),
            ("m6-mfe", "6.3 Micro-Frontends"),
            ("m6-i18n", "6.4 i18n / a11y"),
            ("m6-obs", "6.5 Observability"),
        ],
    },
    {
        "slug": "module-07-case-studies",
        "section_id": "module-7",
        "num": 7,
        "title": "Case Studies",
        "subtitle": "Real-world designs: feeds, chat, docs, video, autocomplete, and e-commerce.",
        "badge": "All levels",
        "subsections": [
            ("cs-feed", "Twitter / News Feed"),
            ("cs-chat", "Chat (WhatsApp/Slack)"),
            ("cs-docs", "Google Docs (Collab)"),
            ("cs-netflix", "Netflix (Video)"),
            ("cs-autocomplete", "Autocomplete / Typeahead"),
            ("cs-ecom", "E-commerce (Amazon)"),
        ],
    },
    {
        "slug": "module-08-interview-playbook",
        "section_id": "module-8",
        "num": 8,
        "title": "Interview Playbook",
        "subtitle": "Format, rubric, tips, question bank, and company-specific questions.",
        "badge": "All levels",
        "subsections": [
            ("m8-format", "8.1 Format & Rubric"),
            ("m8-tips", "8.2 Tips & Anti-patterns"),
            ("m8-bank", "8.3 Question Bank"),
            ("m8-company", "8.4 Company-Specific Questions"),
        ],
    },
]

STYLE_BLOCK = """<link rel="icon" href="/logo.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="/logo.svg" />
<link rel="stylesheet" href="/assets/course.css" />
<style>
  :root{
    --bg:#0f1115; --panel:#171a21; --panel2:#1d212b; --text:#e6e8ef; --muted:#9aa3b2;
    --accent:#7cc4ff; --accent2:#9d7cff; --green:#7ce0a8; --yellow:#ffd479; --red:#ff8a8a;
    --border:#2a2f3a; --code:#0b0d12;
  }
  *{box-sizing:border-box}
  html{font-size:16px;-webkit-text-size-adjust:100%;text-size-adjust:100%}
  html,body{margin:0;padding:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6}
  body{font-size:1rem;padding-bottom:48px}
  a{color:var(--accent);text-decoration:none}
  a:hover{text-decoration:underline}
  h3{font-size:19px;margin:24px 0 8px;color:var(--text)}
  h4{font-size:16px;margin:18px 0 6px;color:var(--accent2)}
  p{margin:8px 0}
  code{background:var(--code);padding:2px 6px;border-radius:4px;font-family:"SF Mono",Menlo,Consolas,monospace;font-size:13px;color:#e0a679}
  pre{background:var(--code);padding:14px 16px;border-radius:8px;overflow-x:auto;border:1px solid var(--border);font-size:13px;line-height:1.5}
  pre code{background:none;padding:0;color:#dbe1ec}
  .pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600;margin-right:6px}
  .pill.basic{background:#1b3b2b;color:var(--green)}
  .pill.inter{background:#3b3b1b;color:var(--yellow)}
  .pill.adv{background:#3b1b2b;color:var(--red)}
  .callout{border-left:3px solid var(--accent);background:var(--panel);padding:12px 16px;margin:14px 0;border-radius:0 8px 8px 0}
  .callout.warn{border-color:var(--yellow)} .callout.tip{border-color:var(--green)}
  .callout strong{color:var(--accent)} .callout.warn strong{color:var(--yellow)} .callout.tip strong{color:var(--green)}
  details.q{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:10px 14px;margin:10px 0}
  details.q summary{cursor:pointer;font-weight:600;color:var(--accent2)}
  details.q[open]{background:var(--panel2)}
  details.q .answer{margin-top:10px;padding-top:10px;border-top:1px dashed var(--border)}
  .walkthrough{counter-reset:step}
  .walkthrough .step{position:relative;padding:10px 12px 10px 38px;margin:8px 0;background:var(--code);border-radius:6px;border-left:3px solid var(--accent2)}
  .walkthrough .step::before{counter-increment:step;content:counter(step);position:absolute;left:10px;top:10px;width:20px;height:20px;background:var(--accent2);color:#0b0d12;border-radius:50%;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center}
  .walkthrough .step .label{display:block;font-weight:600;color:var(--accent);font-size:12px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}
  .walkthrough .step .label.script{color:var(--green)}
  .walkthrough .step p{margin:4px 0;font-size:13.5px}
  .script-line{font-style:italic;color:#cdd5e3;border-left:2px solid var(--green);padding-left:10px;margin:6px 0;font-size:13.5px}
  .followup{margin-top:10px;padding:10px 12px;background:var(--panel);border-radius:6px;font-size:13px}
  .followup strong{color:var(--yellow)}
  .company-tags{display:inline-flex;gap:5px;flex-wrap:wrap;margin-left:8px;vertical-align:middle}
  .ctag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10.5px;font-weight:600;letter-spacing:0.3px;text-transform:uppercase;border:1px solid transparent}
  .ctag.meta{background:#1a2540;color:#7eb6ff;border-color:#2a4570}
  .ctag.google{background:#1f2a1c;color:#9ad48a;border-color:#3a5a32}
  .ctag.microsoft{background:#1f2933;color:#7cd1e0;border-color:#345566}
  .ctag.amazon{background:#332416;color:#ffb86b;border-color:#664a2c}
  .ctag.apple{background:#2a2a2a;color:#d8d8d8;border-color:#555}
  .ctag.netflix{background:#3a1a1f;color:#ff9aa2;border-color:#6a2a35}
  .ctag.uber{background:#1a1a1a;color:#e0e0e0;border-color:#444}
  .ctag.agoda{background:#2a1a3a;color:#c9a3ff;border-color:#5a3580}
  .ctag.airbnb{background:#3a1a26;color:#ff9ab8;border-color:#6a2a48}
  .ctag.stripe{background:#1c2a3f;color:#9ab8ff;border-color:#345878}
  .ctag.atlassian{background:#1a2540;color:#8eb4ff;border-color:#2c4880}
  .ctag.bytedance{background:#2a2030;color:#ff9ad1;border-color:#553560}
  .ctag.linkedin{background:#1a2a3a;color:#8ec5ff;border-color:#2c4a70}
  .ctag.shopify{background:#1f2e1f;color:#9ad48a;border-color:#3a5a3a}
  .ctag.booking{background:#1a2a40;color:#7ab0ff;border-color:#2c4a78}
  .ctag.salesforce{background:#1a2a3a;color:#7ec5ff;border-color:#2c4a70}
  .ctag.tiktok{background:#1a1a1a;color:#ff7eb6;border-color:#553060}
  table{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px}
  th,td{border:1px solid var(--border);padding:8px 10px;text-align:left;vertical-align:top}
  th{background:var(--panel);color:var(--accent)}
  ul.clean li{margin:4px 0}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .site-footer-bar{position:fixed;bottom:0;left:0;right:0;z-index:200;padding:10px 16px;background:var(--panel);text-align:center;font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px 10px}
  .site-footer-bar strong{color:var(--accent)}
  .site-footer-bar a{color:var(--muted);text-decoration:none;font-weight:500}
  .site-footer-bar a:hover{color:var(--accent);text-decoration:underline}
  .site-footer-bar .footer-sep{color:var(--border)}
  .site-footer-bar .footer-author{color:inherit}
  .site-footer-bar .footer-author strong{color:var(--accent)}
  @media (max-width:900px){.grid2{grid-template-columns:1fr} pre{overflow-x:auto;-webkit-overflow-scrolling:touch} th,td{word-break:break-word}}
</style>"""

FOOTER = """
<footer class="site-footer-bar">
  <span>Created with ❤️ by <a href="https://www.linkedin.com/in/sourabh-rajwade-60b5a2b9/" target="_blank" rel="noopener noreferrer" class="footer-author"><strong>Sourabh Rajwade</strong></a></span>
  <span class="footer-sep">·</span>
  <a href="https://x.com/RajwadeSourabh" target="_blank" rel="noopener noreferrer">Twitter / X</a>
  <span class="footer-sep">·</span>
  <a href="https://www.linkedin.com/in/sourabh-rajwade-60b5a2b9/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
</footer>
<script src="/assets/analytics.js"></script>
<script src="/assets/course.js"></script>
</body></html>"""


def extract_sections(html: str) -> dict[str, str]:
    sections = {}
    for ch in CHAPTERS:
        sid = ch["section_id"]
        pattern = rf'<section id="{sid}">(.*?)</section>'
        m = re.search(pattern, html, re.DOTALL)
        if not m:
            raise SystemExit(f"Missing section {sid}")
        sections[sid] = m.group(1).strip()
    return sections


def render_sidebar(active_slug: str) -> str:
    parts = [
        '<aside class="course-sidebar" id="course-sidebar">',
        '<a href="/" class="hub-link"><img src="/logo.svg" alt="Learning Hub" class="hub-logo" width="24" height="24" /> Learning Hub</a>',
        '<div class="course-brand">',
        f'<h1><a href="{COURSE_PREFIX}/index.html" style="color:inherit;text-decoration:none">FE System Design</a></h1>',
        '<p class="sub">Basics → Advanced · with examples &amp; interview Qs</p>',
        "</div>",
        '<span class="toc-label">Table of Contents</span>',
        '<nav class="toc-panel">',
    ]
    for ch in CHAPTERS:
        active = " active" if ch["slug"] == active_slug else ""
        parts.append(
            f'<a class="toc-chapter-link{active}" href="{COURSE_PREFIX}/{ch["slug"]}.html">Module {ch["num"]} · {ch["title"]}</a>'
        )
        if ch["slug"] == active_slug:
            parts.append("<ul class=\"toc-sub\">")
            for anchor, label in ch["subsections"]:
                parts.append(f'<li><a href="#{anchor}">{label}</a></li>')
            parts.append("</ul>")
    parts.append("</nav>")
    parts.append("""
<div class="course-progress" id="course-progress">
  <div class="course-progress-header">
    <span class="course-progress-label">Course Progress</span>
    <span class="course-progress-pct" id="progress-pct">0%</span>
  </div>
  <div class="course-progress-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" id="progress-bar">
    <div class="course-progress-fill" id="progress-fill"></div>
  </div>
  <span class="course-progress-meta" id="progress-meta">0 of 8 modules completed</span>
  <button type="button" class="course-progress-clear" id="progress-clear">Clear progress</button>
</div>""")
    parts.append("</aside>")
    return "\n".join(parts)


def render_chapter_page(ch: dict, body: str, prev_ch: Optional[dict], next_ch: Optional[dict]) -> str:
    nav = ['<nav class="chapter-nav">']
    if prev_ch:
        nav.append(
            f'<a href="{COURSE_PREFIX}/{prev_ch["slug"]}.html">← Module {prev_ch["num"]}: {prev_ch["title"]}</a>'
        )
    else:
        nav.append("<span></span>")
    if next_ch:
        nav.append(
            f'<a class="next" href="{COURSE_PREFIX}/{next_ch["slug"]}.html">Module {next_ch["num"]}: {next_ch["title"]} →</a>'
        )
    nav.append("</nav>")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>Module {ch['num']} · {ch['title']} — Frontend System Design</title>
<meta name="description" content="{ch['subtitle']}" />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#0f1115" />
{STYLE_BLOCK}
</head>
<body>
<div class="course-topbar">
  <a class="course-topbar-brand" href="{COURSE_PREFIX}/index.html"><img src="/logo.svg" alt="Learning Hub" width="28" height="28" /> FE System Design</a>
  <button type="button" class="toc-toggle" id="toc-toggle" aria-label="Open table of contents">☰ Contents</button>
</div>
<div class="course-overlay" id="course-overlay"></div>
<div class="course-shell">
{render_sidebar(ch['slug'])}
<main class="course-main">
<header class="chapter-header">
  <div class="chapter-badges"><span class="chapter-badge">{ch['badge']}</span><span class="chapter-badge">Module {ch['num']}</span></div>
  <h1 class="chapter-title">Module {ch['num']} · {ch['title']}</h1>
  <p class="chapter-subtitle">{ch['subtitle']}</p>
</header>
<article class="chapter-body">
<section id="{ch['section_id']}">
{body}
</section>
</article>
{''.join(nav)}
</main>
</div>
{FOOTER}"""


def render_index() -> str:
    cards = []
    for ch in CHAPTERS:
        cards.append(
            f"""<a class="course-index-card" href="{COURSE_PREFIX}/{ch['slug']}.html">
  <span class="num">Module {ch['num']}</span>
  <h2>{ch['title']}</h2>
  <p>{ch['subtitle']}</p>
</a>"""
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>Frontend System Design — Course Overview</title>
<meta name="description" content="Multi-chapter frontend system design course with modules on architecture, performance, CDNs, security, case studies, and interview prep." />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#0f1115" />
{STYLE_BLOCK}
</head>
<body>
<div class="course-topbar">
  <a class="course-topbar-brand" href="/"><img src="/logo.svg" alt="Learning Hub" width="28" height="28" /> Learning Hub</a>
  <button type="button" class="toc-toggle" id="toc-toggle" aria-label="Open table of contents">☰ Chapters</button>
</div>
<div class="course-overlay" id="course-overlay"></div>
<div class="course-shell">
{render_sidebar("")}
<main class="course-main">
<header class="chapter-header">
  <div class="chapter-badges"><span class="chapter-badge">Course</span><span class="chapter-badge">8 Modules</span></div>
  <h1 class="chapter-title">Frontend System Design</h1>
  <p class="chapter-subtitle">From the browser rendering pipeline to designing Twitter at scale — pick a chapter from the sidebar or cards below.</p>
</header>
<div class="course-index-grid">
{chr(10).join(cards)}
</div>
</main>
</div>
{FOOTER}"""


def main():
    html = SOURCE.read_text(encoding="utf-8")
    sections = extract_sections(html)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(render_index(), encoding="utf-8")
    for i, ch in enumerate(CHAPTERS):
        prev_ch = CHAPTERS[i - 1] if i > 0 else None
        next_ch = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
        page = render_chapter_page(ch, sections[ch["section_id"]], prev_ch, next_ch)
        (OUT / f"{ch['slug']}.html").write_text(page, encoding="utf-8")
    print(f"Generated {len(CHAPTERS) + 1} pages in {OUT}")


if __name__ == "__main__":
    main()
