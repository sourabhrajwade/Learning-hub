#!/usr/bin/env python3
"""Split interview-prep.html into multi-page GenAI course."""

import json
import re
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "interview-prep-source.html"
OUT = ROOT / "interview-prep"

CHAPTERS = [
    {"slug": "module-01-overview", "section_ids": ["overview"], "num": 1, "title": "Overview", "subtitle": "Role overview and what interviewers look for at AVP level.", "badge": "Start here"},
    {"slug": "module-02-ml-foundations", "section_ids": ["foundations"], "num": 2, "title": "ML Foundations", "subtitle": "Machine learning basics before LLMs and agents.", "badge": "Foundations"},
    {"slug": "module-03-genai-foundations", "section_ids": ["genai-foundations"], "num": 3, "title": "GenAI Foundations", "subtitle": "Transformers, tokens, prompting, and how LLMs work.", "badge": "Foundations"},
    {"slug": "module-04-models", "section_ids": ["models"], "num": 4, "title": "Model Landscape", "subtitle": "Open vs closed models, vendors, and selection trade-offs.", "badge": "Models"},
    {"slug": "module-05-python", "section_ids": ["python"], "num": 5, "title": "Python", "subtitle": "Python patterns and libraries for GenAI engineering interviews.", "badge": "Technical"},
    {"slug": "module-06-genai", "section_ids": ["genai"], "num": 6, "title": "Generative AI", "subtitle": "Production GenAI patterns, guardrails, and architecture.", "badge": "GenAI"},
    {"slug": "module-07-agentic", "section_ids": ["agentic"], "num": 7, "title": "Agentic AI", "subtitle": "Agents, tools, planning loops, and orchestration.", "badge": "Agentic"},
    {"slug": "module-08-llms", "section_ids": ["llms"], "num": 8, "title": "LLMs & Tooling", "subtitle": "Inference, fine-tuning, embeddings, and MLOps for LLMs.", "badge": "LLMs"},
    {"slug": "module-09-rag", "section_ids": ["rag"], "num": 9, "title": "RAG Deep-Dive", "subtitle": "Retrieval-augmented generation architecture and patterns.", "badge": "RAG"},
    {"slug": "module-10-advanced-rag", "section_ids": ["arag"], "num": 10, "title": "Advanced RAG", "subtitle": "Hybrid search, re-ranking, query transformation, and agents.", "badge": "RAG"},
    {"slug": "module-11-banking", "section_ids": ["banking"], "num": 11, "title": "Banking Project", "subtitle": "Enterprise banking GenAI case study and talking points.", "badge": "Case study"},
    {"slug": "module-12-eval", "section_ids": ["eval"], "num": 12, "title": "Eval (RAGAS)", "subtitle": "Evaluation frameworks, metrics, and production quality gates.", "badge": "Eval"},
    {"slug": "module-13-langchain", "section_ids": ["langchain"], "num": 13, "title": "LangChain & LangGraph", "subtitle": "LangChain v1, LangGraph, and agent workflows.", "badge": "Tooling"},
    {"slug": "module-14-sdlc", "section_ids": ["sdlc"], "num": 14, "title": "SDLC", "subtitle": "Software delivery for GenAI in enterprise settings.", "badge": "Enterprise"},
    {"slug": "module-15-cloud", "section_ids": ["cloud"], "num": 15, "title": "Cloud-native", "subtitle": "Cloud architecture, deployment, and scaling GenAI systems.", "badge": "Cloud"},
    {"slug": "module-16-databases", "section_ids": ["data"], "num": 16, "title": "Databases", "subtitle": "Vector stores, SQL, and data integration patterns.", "badge": "Data"},
    {"slug": "module-17-copilot", "section_ids": ["copilot"], "num": 17, "title": "GitHub Copilot", "subtitle": "Copilot for engineering productivity and governance.", "badge": "Tooling"},
    {"slug": "module-18-behavioral", "section_ids": ["behavioral"], "num": 18, "title": "Behavioral", "subtitle": "Leadership, stakeholder management, and STAR stories.", "badge": "Interview"},
    {"slug": "module-19-system-design", "section_ids": ["systemdesign"], "num": 19, "title": "System Design", "subtitle": "Designing GenAI solutions for client journeys.", "badge": "Interview"},
    {"slug": "module-20-questions", "section_ids": ["questions"], "num": 20, "title": "Questions to Ask", "subtitle": "Smart questions that signal seniority.", "badge": "Interview"},
    {"slug": "module-21-cheat-sheet", "section_ids": ["cheat"], "num": 21, "title": "Cheat Sheet", "subtitle": "Day-before checklist and phrases that signal seniority.", "badge": "Wrap-up"},
]

MODULE_SLUGS = [c["slug"] for c in CHAPTERS]
COURSE_CONFIG = {
    "storageKey": "learning-hub-genai-progress",
    "moduleSlugs": MODULE_SLUGS,
}

STYLE_BLOCK = """<link rel="icon" href="../logo.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="../logo.svg" />
<link rel="stylesheet" href="../assets/course.css" />
<style>
  :root{
    --bg:#0f1320; --panel:#161b2e; --panel2:#1d2440; --text:#e8ecf8; --muted:#a4adc8;
    --accent:#7c8cff; --accent2:#4ad6c0; --green:#7ee08a; --yellow:#f6a96b; --red:#ff8a8a;
    --border:#2a3357; --code:#0b0f1a;
  }
  *{box-sizing:border-box}
  html{font-size:16px;-webkit-text-size-adjust:100%;text-size-adjust:100%}
  html,body{margin:0;padding:0;background:linear-gradient(180deg,#0a0e19 0%,var(--bg) 100%);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6}
  body{font-size:1rem;padding-bottom:48px}
  a{color:var(--accent);text-decoration:none}
  a:hover{text-decoration:underline}
  h3{font-size:19px;margin:24px 0 8px;color:var(--text)}
  h4{font-size:16px;margin:18px 0 6px;color:var(--accent2)}
  p{margin:8px 0}
  code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
  pre{background:var(--code);border:1px solid var(--border);border-radius:10px;padding:14px;overflow-x:auto;font-size:12.5px;color:#cdd6f4}
  .card{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:18px 20px;margin-bottom:14px}
  .qa{display:grid;grid-template-columns:1fr;gap:10px}
  .q{font-weight:600;color:var(--text);display:flex;gap:10px}
  .q .badge{flex-shrink:0;background:rgba(124,140,255,0.12);color:var(--accent);border:1px solid rgba(124,140,255,0.3);padding:1px 8px;border-radius:6px;font-size:11px;font-weight:600}
  .a{color:var(--muted);border-left:2px solid var(--accent2);padding-left:14px;margin:0}
  .a strong{color:var(--text)}
  .tip{background:rgba(126,224,138,0.08);border:1px solid rgba(126,224,138,0.25);color:var(--green);border-radius:10px;padding:10px 14px;font-size:14px;margin:12px 0}
  .warn{background:rgba(246,169,107,0.08);border:1px solid rgba(246,169,107,0.25);color:var(--yellow);border-radius:10px;padding:10px 14px;font-size:14px;margin:12px 0}
  ul.clean{margin:0;padding-left:20px;color:var(--muted)}
  ul.clean li{margin-bottom:6px}
  ul.clean li strong{color:var(--text)}
  .grid-2{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
  details{border:1px solid var(--border);border-radius:10px;padding:10px 14px;margin-bottom:8px;background:var(--panel2)}
  details summary{cursor:pointer;font-weight:600;color:var(--text);list-style:none}
  details summary::-webkit-details-marker{display:none}
  details summary::before{content:"▸ ";color:var(--accent)}
  details[open] summary::before{content:"▾ "}
  details>*:not(summary){margin-top:10px;color:var(--muted)}
  .star{background:var(--panel2);border:1px solid var(--border);border-radius:10px;padding:14px;margin:12px 0}
  .star b{color:var(--accent)}
  table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--border);border-radius:10px;overflow:hidden;font-size:14px;margin:14px 0}
  th,td{padding:10px 12px;border-bottom:1px solid var(--border);text-align:left;color:var(--muted);vertical-align:top}
  th{background:var(--panel2);color:var(--text);font-weight:600}
  tr:last-child td{border-bottom:none}
  .chapter-body section h2{display:none}
  .chapter-body section .intro{display:none}
  .chapter-body section h2 .num{display:none}
  .site-footer-bar{position:fixed;bottom:0;left:0;right:0;z-index:200;padding:10px 16px;background:var(--panel);text-align:center;font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px 10px}
  .site-footer-bar strong{color:var(--accent)}
  .site-footer-bar a{color:var(--muted);text-decoration:none;font-weight:500}
  .site-footer-bar a:hover{color:var(--accent);text-decoration:underline}
  .site-footer-bar .footer-sep{color:var(--border)}
  .site-footer-bar .footer-author{color:inherit}
  .site-footer-bar .footer-author strong{color:var(--accent)}
  @media (max-width:900px){.grid-2{grid-template-columns:1fr} pre{overflow-x:auto;-webkit-overflow-scrolling:touch} th,td{word-break:break-word}}
</style>"""

FOOTER = """
<footer class="site-footer-bar">
  <span>Created with ❤️ by <a href="https://www.linkedin.com/in/sourabh-rajwade-60b5a2b9/" target="_blank" rel="noopener noreferrer" class="footer-author"><strong>Sourabh Rajwade</strong></a></span>
  <span class="footer-sep">·</span>
  <a href="https://x.com/RajwadeSourabh" target="_blank" rel="noopener noreferrer">Twitter / X</a>
  <span class="footer-sep">·</span>
  <a href="https://www.linkedin.com/in/sourabh-rajwade-60b5a2b9/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
</footer>
<script type="application/json" id="course-config">""" + json.dumps(COURSE_CONFIG) + """</script>
<script src="../assets/course.js"></script>
</body></html>"""


def extract_section(html: str, section_id: str) -> str:
    pattern = rf'<section id="{section_id}">(.*?)</section>'
    m = re.search(pattern, html, re.DOTALL)
    if not m:
        raise SystemExit(f"Missing section {section_id}")
    return m.group(1).strip()


def extract_subsections(content: str) -> List[tuple]:
    subs = []
    for m in re.finditer(r'<h3[^>]*\sid="([^"]+)"[^>]*>(.*?)</h3>', content, re.DOTALL):
        label = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if label:
            subs.append((m.group(1), label[:80]))
    return subs[:12]


def render_sidebar(active_slug: str, chapter_subs: Optional[List[tuple]] = None) -> str:
    parts = [
        '<aside class="course-sidebar" id="course-sidebar">',
        '<a href="../index.html" class="hub-link"><img src="../logo.svg" alt="" class="hub-logo" width="24" height="24" /> Learning Hub</a>',
        '<div class="course-brand">',
        '<h1><a href="index.html" style="color:inherit;text-decoration:none">GenAI &amp; Emerging Tech</a></h1>',
        '<p class="sub">Interview prep · Python · LLMs · RAG · Cloud</p>',
        "</div>",
        '<span class="toc-label">Table of Contents</span>',
        '<nav class="toc-panel">',
    ]
    for ch in CHAPTERS:
        active = " active" if ch["slug"] == active_slug else ""
        parts.append(
            f'<a class="toc-chapter-link{active}" href="{ch["slug"]}.html">Module {ch["num"]} · {ch["title"]}</a>'
        )
        if ch["slug"] == active_slug and chapter_subs:
            parts.append('<ul class="toc-sub">')
            for anchor, label in chapter_subs:
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
  <span class="course-progress-meta" id="progress-meta">0 of 21 modules completed</span>
  <button type="button" class="course-progress-clear" id="progress-clear">Clear progress</button>
</div>""")
    parts.append("</aside>")
    return "\n".join(parts)


def render_chapter_page(ch: dict, body: str, subs: List[tuple], prev_ch: Optional[dict], next_ch: Optional[dict]) -> str:
    nav = ['<nav class="chapter-nav">']
    if prev_ch:
        nav.append(f'<a href="{prev_ch["slug"]}.html">← Module {prev_ch["num"]}: {prev_ch["title"]}</a>')
    else:
        nav.append("<span></span>")
    if next_ch:
        nav.append(f'<a class="next" href="{next_ch["slug"]}.html">Module {next_ch["num"]}: {next_ch["title"]} →</a>')
    nav.append("</nav>")

    if len(ch["section_ids"]) == 1:
        sections_wrapped = f'<section id="{ch["section_ids"][0]}">\n{body}\n</section>'
    else:
        sections_wrapped = body

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<title>Module {ch['num']} · {ch['title']} — GenAI Interview Prep</title>
<meta name="description" content="{ch['subtitle']}" />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#0f1320" />
{STYLE_BLOCK}
</head>
<body>
<div class="course-topbar">
  <a class="course-topbar-brand" href="index.html"><img src="../logo.svg" alt="" width="28" height="28" /> GenAI &amp; Emerging Tech</a>
  <button type="button" class="toc-toggle" id="toc-toggle" aria-label="Open table of contents">☰ Contents</button>
</div>
<div class="course-overlay" id="course-overlay"></div>
<div class="course-shell">
{render_sidebar(ch['slug'], subs)}
<main class="course-main">
<header class="chapter-header">
  <div class="chapter-badges"><span class="chapter-badge">{ch['badge']}</span><span class="chapter-badge">Module {ch['num']}</span></div>
  <h1 class="chapter-title">Module {ch['num']} · {ch['title']}</h1>
  <p class="chapter-subtitle">{ch['subtitle']}</p>
</header>
<article class="chapter-body">
{sections_wrapped}
</article>
{''.join(nav)}
</main>
</div>
{FOOTER}"""


def render_index() -> str:
    cards = []
    for ch in CHAPTERS:
        cards.append(
            f"""<a class="course-index-card" href="{ch['slug']}.html">
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
<title>GenAI &amp; Emerging Tech — Course Overview</title>
<meta name="description" content="Interview preparation for Generative AI roles: Python, LLMs, RAG, Agentic AI, LangChain, cloud-native, and leadership." />
<meta name="robots" content="index, follow" />
<meta name="theme-color" content="#0f1320" />
{STYLE_BLOCK}
</head>
<body>
<div class="course-topbar">
  <a class="course-topbar-brand" href="../index.html"><img src="../logo.svg" alt="" width="28" height="28" /> Learning Hub</a>
  <button type="button" class="toc-toggle" id="toc-toggle" aria-label="Open table of contents">☰ Chapters</button>
</div>
<div class="course-overlay" id="course-overlay"></div>
<div class="course-shell">
{render_sidebar("")}
<main class="course-main">
<header class="chapter-header">
  <div class="chapter-badges"><span class="chapter-badge">Course</span><span class="chapter-badge">21 Modules</span></div>
  <h1 class="chapter-title">GenAI &amp; Emerging Tech</h1>
  <p class="chapter-subtitle">Interview preparation covering Python, Generative AI, Agentic AI, LLMs, RAG, LangChain, cloud-native patterns, and leadership topics.</p>
</header>
<div class="course-index-grid">
{chr(10).join(cards)}
</div>
</main>
</div>
{FOOTER}"""


def main():
    html = SOURCE.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(render_index(), encoding="utf-8")

    for i, ch in enumerate(CHAPTERS):
        parts = [extract_section(html, sid) for sid in ch["section_ids"]]
        body = "\n\n".join(parts)
        subs = extract_subsections(body)
        prev_ch = CHAPTERS[i - 1] if i > 0 else None
        next_ch = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
        page = render_chapter_page(ch, body, subs, prev_ch, next_ch)
        (OUT / f"{ch['slug']}.html").write_text(page, encoding="utf-8")

    print(f"Generated {len(CHAPTERS) + 1} pages in {OUT}")


if __name__ == "__main__":
    main()
