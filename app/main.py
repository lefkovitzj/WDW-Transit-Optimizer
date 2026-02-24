"""
Project Name: WDW-Transit-Optimizer
File Name: app/main.py
Description: Main application entry point for the WDW Transit Optimizer.
Author: Joseph Lefkovitz (github.com/lefkovitzj)
Last Modified: 1/10/2026
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Local imports
from app.core.config import settings
from app.core.graph import GraphManager
from app.routes import router, graph_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Application lifespan context manager. Initializes graph on startup. """
    app.state.graph = GraphManager()
    print("Successfully loaded graph data.")
    yield
    print("Shutting down application.")

# Create the application.
app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)

# Add application routes.
app.include_router(router)
app.include_router(graph_router)

# Mount static files (CSS, JS, images).
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)