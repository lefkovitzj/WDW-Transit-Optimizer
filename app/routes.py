"""
Project Name: WDW-Transit-Optimizer
File Name: app/routes.py
Description: Routes for the WDW Transit Optimizer application.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/10/2026
"""

# Python standard library imports.
from typing import List

# Third-party imports.
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Local imports.
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_graph(request: Request):
    """ Graph state dependency. """
    return request.app.state.graph

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """ Home page route."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "locations": request.app.state.graph.valid_stops,
        "settings": settings
    })

@router.post("/search-locations", response_class=HTMLResponse)
async def search(request: Request, q: str = Form(""), graph=Depends(get_graph)):
    """ HTMX Endpoint: Search for locations matching the query. """
    matches = {
        name: loc_id for name, loc_id in graph.display_names.items()
        if q.lower() in name.lower() and loc_id.endswith("_MAIN")
    }
    print(f"Search query: {q}, Matches found: {len(matches)}")
    return templates.TemplateResponse("components/search_results.html", {
        "request": request,
        "query": q,
        "matches": matches
    })

@router.post("/plan", response_class=HTMLResponse)
async def plan_route(
    request: Request,
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

    # Check if this is an HTMX request
    inverted_display_names = {v: k for k, v in graph.display_names.items()}
    if request.headers.get("HX-Request"):
        print(inverted_display_names)
        return templates.TemplateResponse("components/itinerary.html", {
            "request": request,
            "result": result,
            "display_names": inverted_display_names
        })

    # Fallback for full page reload
    return templates.TemplateResponse("pages/index.html", {
        "request": request,
        "locations": inverted_display_names,
        "result": result
    })
