# sunghwanl.github.io

Personal homepage, built from a YAML file with a small Python script.

## Layout

| Path | What |
|---|---|
| `content.yaml` | All content: profile, sections, publications |
| `templates/index.html` | Jinja2 page template |
| `static/` | Copied as-is to the site root (`style.css`, `cv.pdf`, images, …) |
| `build.py` | Renders everything into `dist/` |

## Build and preview locally

```sh
pip install -r requirements.txt   # once: jinja2, pyyaml, markdown

python build.py                   # build into dist/
python build.py --serve           # build, then serve at http://localhost:8000
python build.py --serve --port 8080
```

There is no auto-reload: after editing, run `python build.py` again (in another
terminal is fine while the server is running) and refresh the browser.

## Deploy

Push to `main`. GitHub Actions (`.github/workflows/gh-pages.yml`) builds the
site and publishes `dist/` to the `gh-pages` branch, which GitHub Pages serves.
`dist/` itself is not committed.
