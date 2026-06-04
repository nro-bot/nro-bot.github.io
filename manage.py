#!/usr/bin/env python
"""
Local browser GUI for editing this Pelican portfolio's project files.

Run:   .venv/bin/python manage.py
Then:  open http://127.0.0.1:5001

It reads/writes content/*.md in Pelican's python-markdown metadata format
(``Key: value`` lines, no YAML fences), preserving field order and body
verbatim. Nothing is committed to git — you commit when you like, as before.
"""
import re
import subprocess
import sys
from pathlib import Path

from flask import Flask, redirect, render_template_string, request, url_for, flash

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
VENV_PELICAN = ROOT / ".venv" / "bin" / "pelican"

CATEGORIES = [
    "Research and Software",
    "Robotics",
    "Hardware/Mechatronics",
    "Leadership",
    "Fun",
    "Press and Other Events",
]

# Known fields shown as first-class form rows, in this display order.
CORE_FIELDS = ["Title", "Date", "Category", "Slug", "Starred", "Summary", "Featured_Image"]
LINK_FIELDS = ["Website", "Code", "Arxiv", "Paper", "Slides", "Video", "Press"]
VIDEO_FIELDS = ["Card_Video", "Card_Video_Autoplay", "Card_Video_Loop", "Tags"]
OPTIONAL_FIELDS = LINK_FIELDS + VIDEO_FIELDS
KNOWN_FIELDS = CORE_FIELDS + OPTIONAL_FIELDS

META_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_]*):\s?(.*)$")


# ---------------------------------------------------------------------------
# Parsing / serialising — preserves field order and the body byte-for-byte.
# ---------------------------------------------------------------------------
def parse(path: Path):
    """Return (ordered list of [key, value], body_str)."""
    lines = path.read_text(encoding="utf-8").split("\n")
    meta, body_start = [], len(lines)
    for i, line in enumerate(lines):
        if line.strip() == "":
            body_start = i + 1
            break
        m = META_RE.match(line)
        if m:
            meta.append([m.group(1), m.group(2)])
        elif meta:  # unindented continuation of the previous value (e.g. EECS)
            meta[-1][1] += "\n" + line
        # a stray first line with no colon would be dropped; none exist here.
    body = "\n".join(lines[body_start:])
    return meta, body


def serialise(meta, body: str) -> str:
    meta_text = "\n".join(f"{k}: {v}" for k, v in meta)
    return meta_text + "\n\n" + body


def meta_get(meta, key, default=""):
    for k, v in meta:
        if k.lower() == key.lower():
            return v
    return default


def slugify(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", title).strip("-")
    return s or "untitled"


# ---------------------------------------------------------------------------
# Project listing
# ---------------------------------------------------------------------------
def list_projects():
    items = []
    for path in sorted(CONTENT.glob("*.md")):
        meta, _ = parse(path)
        items.append(
            {
                "file": path.name,
                "title": meta_get(meta, "Title", path.stem),
                "category": meta_get(meta, "Category", "—"),
                "date": meta_get(meta, "Date", ""),
                "starred": meta_get(meta, "Starred", "false").strip().lower() == "true",
            }
        )
    # group by category order, then starred-first, then newest date
    cat_rank = {c: i for i, c in enumerate(CATEGORIES)}
    items.sort(
        key=lambda x: (
            cat_rank.get(x["category"], 99),
            0 if x["starred"] else 1,
            x["date"],
        ),
        reverse=False,
    )
    # date is ascending above; flip within group by sorting date desc separately
    items.sort(key=lambda x: x["date"], reverse=True)
    items.sort(key=lambda x: (cat_rank.get(x["category"], 99), 0 if x["starred"] else 1))
    return items


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "local-portfolio-editor"


LIST_HTML = """
<!doctype html><meta charset=utf-8><title>Portfolio editor</title>
<style>
 body{font:15px/1.5 system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}
 h1{font-size:1.4rem} a{color:#0a58ca;text-decoration:none} a:hover{text-decoration:underline}
 .cat{margin-top:1.6rem;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#666;border-bottom:1px solid #eee;padding-bottom:.2rem}
 ul{list-style:none;padding:0;margin:.4rem 0} li{padding:.25rem 0;display:flex;gap:.5rem;align-items:baseline}
 .star{color:#e3a008;width:1em} .date{color:#999;font-size:.8rem;margin-left:auto}
 .bar{display:flex;gap:.6rem;align-items:center;margin:1rem 0}
 .btn{display:inline-block;background:#0a58ca;color:#fff;padding:.4rem .8rem;border-radius:6px;border:0;cursor:pointer;font-size:.9rem}
 .btn.secondary{background:#444} .flash{background:#e7f5e7;border:1px solid #aed6ae;padding:.5rem .8rem;border-radius:6px;margin:.6rem 0}
</style>
<h1>Portfolio editor <span style="font-size:.8rem;color:#999">({{items|length}} projects)</span></h1>
{% for m in messages %}<div class=flash>{{m}}</div>{% endfor %}
<div class=bar>
  <a class=btn href="{{url_for('new')}}">+ New project</a>
  <form method=post action="{{url_for('build')}}" style="margin:0"><button class="btn secondary">Build site</button></form>
</div>
{% set ns = namespace(cat=None) %}
{% for it in items %}
  {% if it.category != ns.cat %}{% set ns.cat = it.category %}<div class=cat>{{it.category}}</div><ul>{% endif %}
  <li><span class=star>{{ '★' if it.starred else '' }}</span>
      <a href="{{url_for('edit', name=it.file)}}">{{it.title}}</a>
      <span class=date>{{it.date[:10]}}</span></li>
{% endfor %}
</ul>
"""

EDIT_HTML = """
<!doctype html><meta charset=utf-8><title>{{title}}</title>
<style>
 body{font:15px/1.5 system-ui,sans-serif;max-width:820px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}
 h1{font-size:1.2rem} a{color:#0a58ca;text-decoration:none}
 label{display:block;font-weight:600;margin:.8rem 0 .2rem;font-size:.85rem}
 input[type=text],textarea,select{width:100%;padding:.45rem;border:1px solid #ccc;border-radius:6px;font:inherit;box-sizing:border-box}
 textarea.body{min-height:340px;font-family:ui-monospace,monospace;font-size:13px}
 textarea.sum{min-height:60px} .row{display:flex;gap:1rem} .row>div{flex:1}
 .chk{display:flex;align-items:center;gap:.4rem;margin-top:1.6rem} .chk input{width:auto}
 .opt{display:grid;grid-template-columns:1fr 1fr;gap:.4rem 1rem}
 .opt label{margin:.4rem 0 0} .bar{margin:1.2rem 0;display:flex;gap:.6rem;align-items:center}
 .btn{background:#0a58ca;color:#fff;padding:.5rem 1rem;border:0;border-radius:6px;cursor:pointer;font-size:.95rem}
 .btn.danger{background:#b42318} .muted{color:#999;font-size:.8rem}
 fieldset{border:1px solid #eee;border-radius:8px;margin-top:1rem;padding:.4rem 1rem 1rem}
 legend{font-size:.8rem;color:#666;text-transform:uppercase;letter-spacing:.05em}
</style>
<p><a href="{{url_for('index')}}">← all projects</a></p>
<h1>{{title}} <span class=muted>· {{name}}</span></h1>
{% for m in messages %}<div style="background:#e7f5e7;border:1px solid #aed6ae;padding:.5rem .8rem;border-radius:6px">{{m}}</div>{% endfor %}
<form method=post>
  <label>Title</label><input type=text name=Title value="{{v.Title}}">
  <div class=row>
    <div><label>Date</label><input type=text name=Date value="{{v.Date}}"></div>
    <div><label>Slug</label><input type=text name=Slug value="{{v.Slug}}"></div>
  </div>
  <div class=row>
    <div><label>Category</label>
      <select name=Category>
        {% for c in categories %}<option {{'selected' if c==v.Category else ''}}>{{c}}</option>{% endfor %}
      </select></div>
    <div class=chk><input type=checkbox name=Starred value=true {{'checked' if v.Starred=='true' else ''}}><label style="margin:0">Starred (flagship)</label></div>
  </div>
  <label>Summary <span class=muted>(card blurb)</span></label>
  <textarea class=sum name=Summary>{{v.Summary}}</textarea>
  <label>Featured_Image <span class=muted>(filename inside content/{{slug}}/)</span></label>
  <input type=text name=Featured_Image value="{{v.Featured_Image}}">

  <fieldset><legend>Links & media (leave blank to omit)</legend>
    <div class=opt>
    {% for f in optional %}
      <div><label>{{f}}</label><input type=text name="{{f}}" value="{{v.get(f,'')}}"></div>
    {% endfor %}
    </div>
  </fieldset>

  <label>Body <span class=muted>(Markdown)</span></label>
  <textarea class=body name=__body__>{{body}}</textarea>

  {% if extra %}<p class=muted>Other preserved fields: {{extra|join(', ')}}</p>{% endif %}
  <div class=bar>
    <button class=btn type=submit>Save</button>
    <a class=btn href="{{url_for('index')}}" style="background:#666">Cancel</a>
    <form method=post action="{{url_for('delete', name=name)}}" onsubmit="return confirm('Delete {{name}}? This removes the .md file.')" style="margin-left:auto">
      <button class="btn danger">Delete</button>
    </form>
  </div>
</form>
"""


@app.route("/")
def index():
    return render_template_string(LIST_HTML, items=list_projects(), messages=_pop_flashes())


@app.route("/edit/<name>", methods=["GET", "POST"])
def edit(name):
    path = CONTENT / name
    if not path.exists() or path.suffix != ".md" or path.parent != CONTENT:
        return "Not found", 404
    meta, body = parse(path)
    if request.method == "POST":
        meta, body = _apply_form(meta)
        path.write_text(serialise(meta, body), encoding="utf-8")
        flash(f"Saved {name}")
        return redirect(url_for("edit", name=name))
    v = {k: meta_get(meta, k) for k in KNOWN_FIELDS}
    extra = [k for k, _ in meta if k not in KNOWN_FIELDS]
    return render_template_string(
        EDIT_HTML, name=name, title=v.get("Title") or path.stem, v=v, body=body,
        slug=v.get("Slug") or path.stem, categories=CATEGORIES, optional=OPTIONAL_FIELDS,
        extra=extra, messages=_pop_flashes(),
    )


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        title = request.form.get("Title", "").strip() or "Untitled"
        slug = request.form.get("Slug", "").strip() or slugify(title)
        path = CONTENT / f"{slug}.md"
        if path.exists():
            flash(f"{path.name} already exists — opened it instead.")
            return redirect(url_for("edit", name=path.name))
        meta = [
            ["Title", title],
            ["Date", request.form.get("Date", "").strip()],
            ["Category", request.form.get("Category", CATEGORIES[0])],
            ["Slug", slug],
            ["Starred", "true" if request.form.get("Starred") else "false"],
            ["Summary", ""],
            ["Featured_Image", ""],
        ]
        path.write_text(serialise(meta, ""), encoding="utf-8")
        (CONTENT / slug).mkdir(exist_ok=True)  # image folder
        flash(f"Created {path.name} and content/{slug}/ for images")
        return redirect(url_for("edit", name=path.name))
    return render_template_string(NEW_HTML, categories=CATEGORIES)


@app.route("/delete/<name>", methods=["POST"])
def delete(name):
    path = CONTENT / name
    if path.exists() and path.suffix == ".md" and path.parent == CONTENT:
        path.unlink()
        flash(f"Deleted {name} (image folder left in place)")
    return redirect(url_for("index"))


@app.route("/build", methods=["POST"])
def build():
    pelican = str(VENV_PELICAN) if VENV_PELICAN.exists() else "pelican"
    try:
        r = subprocess.run(
            [pelican, "content", "-o", "output", "-s", "pelicanconf.py"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or ["(no output)"]
        flash(("Build OK — " if r.returncode == 0 else "Build FAILED — ") + tail[-1])
    except Exception as e:  # noqa: BLE001
        flash(f"Build error: {e}")
    return redirect(url_for("index"))


NEW_HTML = """
<!doctype html><meta charset=utf-8><title>New project</title>
<style>body{font:15px/1.5 system-ui,sans-serif;max-width:600px;margin:2rem auto;padding:0 1rem}
 label{display:block;font-weight:600;margin:.8rem 0 .2rem} input,select{width:100%;padding:.45rem;border:1px solid #ccc;border-radius:6px;box-sizing:border-box}
 .btn{background:#0a58ca;color:#fff;padding:.5rem 1rem;border:0;border-radius:6px;margin-top:1rem;cursor:pointer}</style>
<p><a href="/">← all projects</a></p><h1>New project</h1>
<form method=post>
 <label>Title</label><input name=Title required>
 <label>Slug <span style="font-weight:400;color:#999">(blank = from title; becomes the URL + image folder)</span></label><input name=Slug>
 <label>Date <span style="font-weight:400;color:#999">(YYYY-MM-DD HH:MM)</span></label><input name=Date placeholder="2026-06-04 12:00">
 <label>Category</label><select name=Category>{% for c in categories %}<option>{{c}}</option>{% endfor %}</select>
 <label style="display:flex;gap:.4rem;align-items:center;margin-top:1rem"><input type=checkbox name=Starred value=true style="width:auto"> Starred</label>
 <button class=btn>Create & edit</button>
</form>
"""


# ---------------------------------------------------------------------------
def _apply_form(meta):
    """Update existing meta in place from the submitted form; append new
    optional fields; drop optional fields the user cleared. Required core
    fields are always kept. Body comes from the __body__ textarea."""
    form = request.form
    body = form.get("__body__", "").replace("\r\n", "\n")
    present = {k for k, _ in meta}

    def set_field(key, value):
        nonlocal meta
        for row in meta:
            if row[0].lower() == key.lower():
                row[1] = value
                return
        meta.append([key, value])

    # core fields. Values are stored verbatim (no strip) so that opening a
    # file and saving it with no edits is a guaranteed byte-for-byte no-op.
    for f in CORE_FIELDS:
        if f == "Starred":
            if form.get("Starred"):
                set_field("Starred", "true")
            elif "Starred" in present:
                set_field("Starred", "false")  # keep an explicit false if it existed
            # absent + unchecked -> leave absent (Pelican treats missing as false)
        elif f in form:
            set_field(f, form.get(f, ""))

    # optional fields: set if non-empty, else remove
    for f in OPTIONAL_FIELDS:
        val = form.get(f, "").strip()
        if val:
            set_field(f, val)
        elif f in present:
            meta = [row for row in meta if row[0].lower() != f.lower()]

    return meta, body


def _pop_flashes():
    from flask import get_flashed_messages
    return get_flashed_messages()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    print(f"\n  Portfolio editor → http://127.0.0.1:{port}\n  (editing {CONTENT})\n")
    app.run(debug=True, port=port)
