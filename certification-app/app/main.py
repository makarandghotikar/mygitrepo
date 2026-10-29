from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "certifications.json"
APP_DIR = BASE_DIR / "app"

app = FastAPI(title="AI Cert Guide", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


def load_certifications() -> list[dict[str, Any]]:
    """Load the certification catalog from the JSON data file."""
    with DATA_PATH.open("r", encoding="utf-8") as source:
        return json.load(source)


def sort_certifications(items: list[dict[str, Any]], sort_key: str | None) -> list[dict[str, Any]]:
    """Sort the list using a simple field-based value mapping."""
    if sort_key == "cost_asc":
        return sorted(items, key=lambda cert: cert.get("cost_usd", 0) or 0)
    if sort_key == "cost_desc":
        return sorted(items, key=lambda cert: cert.get("cost_usd", 0) or 0, reverse=True)
    if sort_key == "level_asc":
        order = {"foundational": 1, "associate": 2, "professional": 3}
        return sorted(items, key=lambda cert: (order.get(cert.get("level", "").lower(), 99), cert.get("name", "")))
    return sorted(items, key=lambda cert: cert.get("name", "").lower())


def filter_certifications(
    certs: list[dict[str, Any]],
    *,
    search: str | None = None,
    provider: str | None = None,
    level: str | None = None,
    focus_area: str | None = None,
    max_cost: int | None = None,
    sort: str | None = None,
) -> list[dict[str, Any]]:
    """Apply the user-facing filters and sorting rules."""
    text = (search or "").strip().lower()

    filtered: list[dict[str, Any]] = []
    for cert in certs:
        name = (cert.get("name") or "").lower()
        skills = " ".join(cert.get("skills_covered", []) or []).lower()
        haystack = f"{name} {skills}"

        if text and text not in haystack:
            continue
        if provider and cert.get("provider") != provider:
            continue
        if level and cert.get("level") != level:
            continue
        if focus_area and cert.get("focus_area") != focus_area:
            continue
        if max_cost is not None and (cert.get("cost_usd") or 0) > max_cost:
            continue
        filtered.append(cert)

    return sort_certifications(filtered, sort)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    certs = load_certifications()
    providers = sorted({cert["provider"] for cert in certs})
    levels = sorted({cert["level"] for cert in certs})
    focus_areas = sorted({cert["focus_area"] for cert in certs})

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "certifications": sort_certifications(certs, "level_asc"),
            "providers": providers,
            "levels": levels,
            "focus_areas": focus_areas,
        },
    )


@app.get("/api/certifications")
async def get_certifications(
    search: str | None = Query(default=None),
    provider: str | None = Query(default=None),
    level: str | None = Query(default=None),
    focus_area: str | None = Query(default=None),
    max_cost: int | None = Query(default=None, ge=0),
    sort: str | None = Query(default="level_asc"),
):
    certs = filter_certifications(
        load_certifications(),
        search=search,
        provider=provider,
        level=level,
        focus_area=focus_area,
        max_cost=max_cost,
        sort=sort,
    )
    return JSONResponse(content=certs)


@app.get("/health")
async def health_check():
    return {"status": "ok", "certifications_loaded": len(load_certifications())}


@app.get("/certs/{slug}")
async def cert_detail(request: Request, slug: str):
    cert = next((item for item in load_certifications() if item.get("slug") == slug), None)
    if not cert:
        return templates.TemplateResponse(
            "coming_soon.html",
            {
                "request": request,
                "title": "Certification detail",
                "message": "This certification detail page is coming in the next phase.",
            },
        )

    return templates.TemplateResponse(
        "coming_soon.html",
        {
            "request": request,
            "title": cert.get("name", "Certification"),
            "message": "The full certification detail page is planned for the next phase.",
        },
    )


@app.get("/compare")
async def compare_page(request: Request):
    return templates.TemplateResponse(
        "coming_soon.html",
        {
            "request": request,
            "title": "Compare certifications",
            "message": "The comparison table is coming in the next phase.",
        },
    )


@app.get("/roadmaps")
async def roadmaps_page(request: Request):
    return templates.TemplateResponse(
        "coming_soon.html",
        {
            "request": request,
            "title": "Learning roadmaps",
            "message": "The roadmap recommendations are coming in the next phase.",
        },
    )
