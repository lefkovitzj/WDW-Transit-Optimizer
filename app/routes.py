"""
Project Name: WDW-Wayfinder
File Name: app/routes.py
Description: Routes for the WDW Wayfinder application.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/10/2026
"""

# Python standard library imports.
from typing import List
from pathlib import Path
import json

# Third-party imports.
from fastapi import APIRouter, Request, Form, Depends, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

# Local imports.
from app.core.config import settings
from app.database import engine
from app.models import TransitAnalytics

graph_router = APIRouter(tags=["graph"])

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "wdw_graph.json"
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

@graph_router.get("/api/graph")
def get_graph_data():
    if not DATA_PATH.exists():
        raise HTTPException(status_code=404, detail=f"Graph file not found: {DATA_PATH}")
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return JSONResponse(json.load(f))

@graph_router.get("/graph")
def graph_page(request: Request):
    return TEMPLATES.TemplateResponse("graph.html", {"request": request})


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_graph(request: Request):
    """ Graph state dependency. """
    return request.app.state.graph

def log_search(origin: str, dest: str, stops: List[str]):
    """Background worker that uses a fresh session to write analytics."""
    if not settings.ENABLE_ANALYTICS or engine is None:
        return
    with Session(engine) as session:
        new_entry = TransitAnalytics(
            origin_id=origin,
            destination_id=dest,
            intermediate_stops=stops,
            total_steps=len(stops) + 2
        )
        session.add(new_entry)
        session.commit()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """ Home page route."""
    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={
                                        "request": request,
                                        "locations": request.app.state.graph.valid_stops,
                                        "settings": settings
                                    })

@router.get("/ping")
async def ping():
    return {"status": "ok"}

@router.post("/search-locations", response_class=HTMLResponse)
async def search(request: Request, q: str = Form(""), graph=Depends(get_graph)):
    """ HTMX Endpoint: Search for locations matching the query. """
    matches = {
        name: loc_id for name, loc_id in graph.display_names.items()
        if q.lower() in name.lower() and loc_id.endswith("_MAIN")
    }
    print(f"Search query: {q}, Matches found: {len(matches)}")
    return templates.TemplateResponse(
        request=request,
        name="components/search_results.html", 
        context={
            "request": request,
            "query": q,
            "matches": matches
        })

@router.post("/plan", response_class=HTMLResponse)
async def plan_route(
    request: Request,
    background_tasks: BackgroundTasks,
    start: str = Form(...),
    end: str = Form(...),
    stops: List[str] = Form([]),
    graph=Depends(get_graph)
):
    """ Use custom TSP and Djikstra's logic to plan an optimized route. """
    # Filter out empty stops
    valid_stops = [s for s in stops if s.strip()]

    # Run the TSP/Dijkstra logic
    result = graph.plan_itinerary(start, end, valid_stops)

    # Queue analytics write in the background
    path_stops = result.get("path", valid_stops) if isinstance(result, dict) else valid_stops
    background_tasks.add_task(log_search, start, end, path_stops)

    # Check if this is an HTMX request
    inverted_display_names = {v: k for k, v in graph.display_names.items()}
    if request.headers.get("HX-Request"):
        print(inverted_display_names)
        return templates.TemplateResponse(
            request=request,
            name="components/itinerary.html",
            context={
            "request": request,
            "result": result,
            "display_names": inverted_display_names
        })

    # Fallback for full page reload
    return templates.TemplateResponse(
        request=request,
        name="pages/index.html",
        context={
            "request": request,
            "locations": inverted_display_names,
            "result": result
        })

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "about.html",
        context={"request": request}
    )

@router.get("/contribute", response_class=HTMLResponse)
async def contribute_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contribute.html",
        context={"request": request}
    )

@router.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={"request": request}
    )
