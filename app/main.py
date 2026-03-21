"""
Project Name: WDW-Wayfinder
File Name: app/main.py
Description: Main application entry point for the WDW Wayfinder.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/10/2026
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from app.core.config import settings
from app.core.graph import GraphManager
from app.routes import router, graph_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Application lifespan context manager. Initializes graph on startup. """
    app.state.graph = GraphManager()
    app.state.ga4_measurement_id = settings.GA4_MEASUREMENT_ID
    print("Successfully loaded graph data.")
    yield
    print("Shutting down application.")

# Create the application.
app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)

# Setup for CORS.
origins = [
    settings.PRODUCTION_URL,
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows GET, POST, etc.
    allow_headers=["*"],  # Allows all headers (like Content-Type)
)

# Add application routes.
app.include_router(router)
app.include_router(graph_router)

# Mount static files (CSS, JS, images).
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)