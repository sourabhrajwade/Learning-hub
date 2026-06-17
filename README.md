# Learning Hub

A static study guide site for interview prep and deep-dive technical courses. No build step, no dependencies — just HTML files you can open locally or deploy to Vercel.

## What's included

| Page | File | Description |
|------|------|-------------|
| **Home** | `index.html` | Landing page with cards linking to each course |
| **Frontend System Design** | `frontend-system-design/` | 8 chapter pages with sidebar TOC — architecture, performance, CDNs, security, case studies, interview playbook |
| **GenAI & Emerging Tech** | `genai/` | 21 chapter pages with sidebar TOC — Python, Generative AI, Agentic AI, LLMs, RAG, LangChain, cloud-native patterns, and leadership topics |

Each course page includes a **← Learning Hub** link back to the home page.

## Project structure

```
Learning-hub/
├── logo.svg
├── assets/icon-fe.svg
├── assets/icon-genai.svg
├── index.html
├── assets/course.css
├── assets/course.js
├── assets/analytics.js                 # Vercel Web Analytics (enable in dashboard)
├── frontend-system-design/             # FE course chapters
├── genai/                              # GenAI course chapters
├── genai-source.html                   # Source for regenerating GenAI pages
├── scripts/split-fe-course.py
├── scripts/split-genai-course.py
├── robots.txt
├── sitemap.xml
├── vercel.json
└── README.md
```

## Run locally

Open any HTML file directly in your browser:

```bash
open index.html
```

Or serve the folder with a simple HTTP server:

```bash
# Python 3
python3 -m http.server 8000

# Then visit http://localhost:8000
```

## Deploy to Vercel

This project is a static site. Vercel serves the files as-is — no build command or framework required.

### Option 1 — GitHub + Vercel Dashboard

1. Push this repo to GitHub.
2. Go to [vercel.com](https://vercel.com) and create a **New Project**.
3. Import the repository.
4. Leave build settings empty (no build command, output directory is the repo root).
5. Deploy. Your site will be live at `https://<project-name>.vercel.app`.

### Option 2 — Vercel CLI

```bash
npx vercel        # preview deployment
npx vercel --prod # production deployment
```

### Clean URLs

`vercel.json` enables clean URLs on Vercel, so pages are available without the `.html` extension. Course pages use **root-relative links** (e.g. `/frontend-system-design/module-01-foundations`) so navigation works correctly with Vercel clean URLs.

- `/` → `index.html`
- `/frontend-system-design` → FE course overview
- `/frontend-system-design/module-01-foundations` → FE chapter pages
- `/genai` → GenAI course overview
- `/genai/module-01-overview` → GenAI chapter pages

Legacy URLs redirect automatically: `/interview-prep` → `/genai`, `/frontend-system-design-course` → `/frontend-system-design`.

### Web Analytics

[Vercel Web Analytics](https://vercel.com/docs/analytics) is wired via `assets/analytics.js` on every page. After deploying:

1. Open your project in the [Vercel dashboard](https://vercel.com/dashboard)
2. Go to **Analytics** → **Enable**
3. Visit the live site — page views should appear within ~30 seconds

No npm packages or build step required for this static HTML setup.

## SEO

Each HTML page includes `meta description`, Open Graph, and Twitter Card tags.

| File | Purpose |
|------|---------|
| `robots.txt` | Tells crawlers they may index all pages; points to the sitemap |
| `sitemap.xml` | Lists all public URLs for Google Search Console and other crawlers |

After your first Vercel deploy, update `sitemap.xml` — replace `https://learning-hub.vercel.app` with your live URL (e.g. `https://your-project.vercel.app`). Then submit the sitemap in [Google Search Console](https://search.google.com/search-console): `https://your-project.vercel.app/sitemap.xml`.

## Tech stack

- Plain HTML + inline CSS
- No JavaScript framework, package manager, or build pipeline
- Hosted as static files on [Vercel](https://vercel.com)
