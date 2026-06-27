# Nancy Ouyang — Portfolio (nrobot.dev)

The new personal portfolio for **nrobot.dev**, a static site built with
[Pelican](https://getpelican.com) (Python 3.8+). It replaces the previous
Jekyll site; see [Deployment](#deployment-nrobotdev) below.

The site presents projects as a filterable, Netflix-style gallery: category
tabs, full-text search, year-range filters, a "starred" highlights view, and
per-project pages with link buttons, images, and self-hosted video.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install .            # build deps: pelican[markdown] >= 4.9
pip install ".[editor]"  # optional: + Flask, for the project editor GUI

make html        # build to output/
make serve       # preview at http://localhost:8000
make devserver   # build + auto-reload on changes (port 8000)
make edit        # open the project editor GUI at http://localhost:5001
make clean       # remove output/
```

> Note: always preview with `make serve` (HTTP), not by opening the HTML
> files directly. With `SITEURL = ''` the CSS/JS only resolve over HTTP.

## Project structure

```
portfolio-pelican/
├── content/
│   ├── pages/
│   │   └── about.md                 # About page: bio + skill tags w/ icons
│   ├── Digger-Finger.md             # one project = one markdown file
│   ├── Digger-Finger/               # that project's assets (images, video)
│   │   ├── digger_finger.jpg
│   │   └── ...
│   └── images/
│       ├── face.jpg                 # header avatar
│       └── icons/                   # skill favicons (About page)
├── theme/
│   ├── templates/                   # base, index, article, category, page
│   └── static/css/style.css         # all styling
├── pelicanconf.py                   # config (author, links, static paths)
├── Makefile                         # build / serve / deploy / edit targets
├── manage.py                        # local browser editor for projects
└── pyproject.toml                   # dependencies (pip install ".[editor]")
```

Each project is a markdown file in `content/` plus a same-named asset folder
(e.g. `Throwdini.md` + `Throwdini/`). Asset folders are exposed by listing
them in `STATIC_PATHS` in `pelicanconf.py` — **add new project folders there**
or their images/videos won't be copied to the build.

## Adding or editing a project

You can use the **GUI editor** (below) or edit the markdown **by hand**.

### GUI editor

A small local web app (`manage.py`) that speaks this site's exact Pelican
metadata format, so you can add and edit projects in a browser without
hand-editing front matter:

```bash
pip install ".[editor]"   # one-time: installs Flask
make edit                 # or: python manage.py  →  http://127.0.0.1:5001
```

It lists projects grouped by category (starred-first), gives a form with a
category dropdown, a Starred checkbox, link/media fields, and a Markdown body
box, then writes back `content/*.md` **byte-for-byte** in the same format
(opening and saving a file with no edits produces zero diff). "+ New project"
scaffolds the markdown file and its asset folder; a "Build site" button runs
Pelican. It only touches `content/` — commit when you're ready, just like
hand-editing.

> After creating a project, add its asset folder to `STATIC_PATHS` in
> `pelicanconf.py` (the editor makes the folder but does not edit config), or
> its images/videos won't be copied to the build.

### By hand

Projects use Pelican metadata in the markdown front matter. Custom keys
(everything past `Summary`) are read by the templates to build cards and
link buttons.

```markdown
Title: Digger Finger: GelSight Tactile Sensor
Date: 2020-05-26 12:00
Category: Research and Software
Slug: Digger-Finger
Summary: One- or two-sentence blurb shown on the card and project page.
Featured_Image: digger_finger.jpg      # filename inside the project folder
Starred: true                          # show in the default "starred" view
Card_Video: clip.mp4                    # optional: autoplay video as the thumbnail
Arxiv: https://arxiv.org/abs/...        # link buttons (any subset, see below)
Code: https://github.com/...
Website: https://...
Press: https://...
Slides: https://...
Video: https://...                      # external video link (button only)
Paper: https://....pdf

*Byline / author line in italics.*

Body markdown. Embed self-hosted video with a plain <video> tag:

<video controls muted loop playsinline style="width:100%;border-radius:6px;">
  <source src="/Digger-Finger/clip.mp4" type="video/mp4">
</video>
```

Field reference:

| Field | Purpose |
|---|---|
| `Featured_Image` | Card thumbnail + project-page hero. Required. ~258×153 display; `object-fit: cover`. |
| `Starred` | `true` includes the project in the default highlights view. |
| `Card_Video` | Optional MP4 (in the project folder) that autoplays muted/looped as the card thumbnail, with `Featured_Image` as the poster. |
| `Arxiv` `Code` `Website` `Press` `Slides` `Video` `Paper` | Each renders a link button on the card (max 3, in that priority order) and on the project page. |

**Categories** in use: `Research and Software`, `Robotics`,
`Hardware/Mechatronics`, `Leadership`, `Fun`, `Press and Other Events`. To add
a category, add it to the tab list in `theme/templates/base.html` and to
`ordered_cats` / `cat_descs` in `theme/templates/index.html`. (The GUI editor's
dropdown reads its list from `CATEGORIES` in `manage.py` — update it there too.)

**Videos**: keep them small. Re-encode with ffmpeg, e.g.:

```bash
ffmpeg -i in.mp4 -an -vf "scale='min(720,iw)':-2" -c:v libx264 -crf 28 \
  -preset slower -movflags +faststart out.mp4
```

## Configuration

Edit `pelicanconf.py`:

- `AUTHOR`, `SITENAME`, `SITESUBTITLE` — name and header tagline.
- `EMAIL`, `GITHUB_URL`, `LINKEDIN_URL`, `BLOG_URL` — header contact links.
- `AVATAR` — header avatar path (`/images/face.jpg`).
- `SITEURL` — base URL. Leave `''` for local dev; set the deployed URL for
  production (see below).
- `STATIC_PATHS` — must list every project asset folder.

## Deployment (nrobot.dev)

This repo's **Pelican source** lives in
[`nro-bot/nro-bot.github.io`](https://github.com/nro-bot/nro-bot.github.io/),
and GitHub builds and serves it automatically. `nrobot.dev` is an apex custom
domain, which serves a single repository at the domain root; for a personal
account that root repo is the user-site repo (`nro-bot.github.io`), so putting
the source there is exactly what makes the site appear at `nrobot.dev/`.

GitHub Pages can't run Pelican natively (its built-in build only runs Jekyll),
so a **GitHub Actions workflow** builds the site on each push. This is the
recommended way to use a non-Jekyll generator, and it means the repo holds the
*source* — you never commit the `output/` directory.

### One-time setup

1. Push this project to `nro-bot.github.io` on the `main` branch (source files
   only — `output/` is git-ignored / not committed):

   ```bash
   git remote add origin git@github.com:nro-bot/nro-bot.github.io.git
   git add -A && git commit -m "Pelican portfolio source"
   git push -u origin main
   ```

2. In **Settings → Pages**, set **Source** to **GitHub Actions** (not "Deploy
   from a branch").

3. Set **Custom domain** to `nrobot.dev` and enable **Enforce HTTPS**. Apex DNS
   should have GitHub's `A`/`AAAA` (or `ALIAS`) records; a `www` CNAME →
   `nro-bot.github.io` is recommended so `www.nrobot.dev` redirects to the apex.

### How a deploy happens

The workflow at `.github/workflows/pelican.yml` runs on every push to `main`
(and via manual "Run workflow"). It uses Pelican's official reusable workflow
to install dependencies, build with `publishconf.py`, and publish the result to
Pages:

```yaml
jobs:
  deploy:
    uses: "getpelican/pelican/.github/workflows/github_pages.yml@main"
    permissions: { contents: read, pages: write, id-token: write }
    with:
      settings: "publishconf.py"
      requirements: "."          # installs deps from pyproject.toml
```

Dependencies live in **`pyproject.toml`** (`[project.dependencies]`), and the
workflow installs them with `pip install .` — so CI and a local
`pip install .` use the exact same versions. Bump the dependency in one place.

So the everyday workflow is just:

```bash
# edit content/ or theme/, then:
git add -A && git commit -m "Update project" && git push
```

GitHub builds and deploys within a minute or two. You can even edit content
files in GitHub's web UI and the commit will trigger a deploy.

### Config split

- `pelicanconf.py` — base config; `SITEURL = ''` for local preview.
- `publishconf.py` — imports the base config and sets
  `SITEURL = 'https://nrobot.dev'` with `RELATIVE_URLS = False`. The workflow
  (and `make publish`, if you add it) build with this file so production links
  and assets are absolute. Local `make html` / `make serve` keep using
  `pelicanconf.py`, so previews still work over `http://localhost:8000`.

### Verifying after deploy

- `https://nrobot.dev/` → this portfolio.
- The Actions tab shows each build; a red run means the build failed (the site
  keeps serving the last good deploy).

> The bundled `make github` target (push `output/` to a `gh-pages` branch) is
> an alternative "build-locally" path. It is **not** needed with the Actions
> workflow above and isn't used for nrobot.dev.

## Credits

The site reorganization (category structure, starred-first ordering) and the
project editor (`manage.py`) were developed with
[Claude Opus 4.8](https://claude.com/claude-code) (Anthropic).

