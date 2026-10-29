# AI Cert Guide

AI Cert Guide is a simple FastAPI-based catalog for comparing AI certifications. It helps beginners, career switchers, and IT professionals choose a certification based on provider, level, area of focus, and cost.

## Features

- Home page with live search and filters
- Certification detail route for a single exam
- Compare page for up to three certifications side by side
- Learning roadmaps page
- Dark/light mode support
- JSON-driven data model for easy expansion

## Run locally

From the repository root in PowerShell:

```powershell
. .\certification-app\scripts\activate.ps1
python -m pip install -r .\certification-app\requirements.txt
python -m uvicorn --app-dir .\certification-app app.main:app --reload
```

The activation script creates the repository's `.venv` if needed and activates it in the current PowerShell session. Then open http://127.0.0.1:8000 in your browser.

## Project structure

```text
app/
  __init__.py
  main.py
  routes/
  static/
  templates/
data/
  certifications.json
Dockerfile
requirements.txt
README.md
```

## Add a new certification

1. Open `data/certifications.json`.
2. Add a new object to the array with the required fields:
   - name
   - slug
   - provider
   - level
   - focus_area
   - exam_code
   - cost_usd
   - exam_duration
   - prerequisites
   - recommended_experience
   - skills_covered
   - official_url
   - learning_resources_url
   - who_its_for
   - last_verified
3. Keep the `slug` unique and URL-safe.
4. Restart the app or use `--reload` for live updates.

## Notes

- The catalog data is loaded at startup from the JSON file.
- Details are intentionally easy to edit so new certifications can be added without changing server logic.
- Always confirm pricing and exam requirements on the official provider site before registering.
