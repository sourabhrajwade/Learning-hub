# Learning Hub

A static study guide site for interview prep and deep-dive technical courses. No build step, no dependencies — just HTML files you can open locally or deploy to Vercel.

## What's included

| Page | File | Description |
|------|------|-------------|
| **Home** | `index.html` | Landing page with cards linking to each course |
| **Frontend System Design** | `frontend-system-design-course.html` | Browser fundamentals through architecture, performance, CDNs, security, scalability, case studies, and interview playbook |
| **GenAI & Emerging Tech** | `interview-prep.html` | Python, Generative AI, Agentic AI, LLMs, RAG, LangChain, cloud-native patterns, and leadership topics |

Each course page includes a **← Learning Hub** link back to the home page.

## Project structure

```
Learning-hub/
├── index.html                          # Homepage
├── frontend-system-design-course.html  # Frontend system design course
├── interview-prep.html                 # GenAI & emerging tech interview prep
├── robots.txt                          # Search engine crawl rules
├── sitemap.xml                         # Page list for Google & other crawlers
├── vercel.json                         # Vercel static site config
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

`vercel.json` enables clean URLs on Vercel, so pages are available without the `.html` extension:

- `/` → `index.html`
- `/frontend-system-design-course` → `frontend-system-design-course.html`
- `/interview-prep` → `interview-prep.html`

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
