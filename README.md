<!-- PROJECT SHIELDS -->
[![Python][python-shield]][python-url]
[![FastAPI][fastapi-shield]][fastapi-url]
[![HTMX][htmx-shield]][htmx-url]
[![Docker][docker-shield]][docker-url]

<br />
<div align="center">
  <h3 align="center">WDW Wayfinder</h3>

  <p align="center">
    A FastAPI web app that computes optimized Walt Disney World transit itineraries using Dijkstra + Held-Karp TSP.
    <br />
    <a href="https://github.com/lefkovitzj/WDW_Transit_Optimizer"><strong>Explore the repo »</strong></a>
    <br />
    <br />
    <a href="#usage">View Demo Flow</a>
    ·
    <a href="https://github.com/lefkovitzj/WDW_Transit_Optimizer/issues">Report Bug</a>
    ·
    <a href="https://github.com/lefkovitzj/WDW_Transit_Optimizer/issues">Request Feature</a>
  </p>
</div>

---

## About The Project

WDW Wayfinder helps plan Disney transit routes between resorts, parks, and hubs.  
It combines:

- **Mode-aware shortest paths** (Dijkstra)
- **Optimal stop ordering** (Held-Karp TSP)
- **Interactive graph visualization** (vis-network)
- **Search-driven UX** (HTMX + server-side templates)

Core implementation lives in:
- [app/core/graph.py](app/core/graph.py)
- [app/routes.py](app/routes.py)
- [app/main.py](app/main.py)

---

## Built With

- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [HTMX](https://htmx.org/)
- [vis-network](https://visjs.github.io/vis-network/docs/network/)
- [Docker](https://www.docker.com/)
- Python 3.11

### Development Workflow

This project is one of my first attempts at partially using AI-assisted development while building an application.  
AI tools such as GitHub copilot were used to help brainstorm, prototype, and refactor parts of the code - especially the frontend design and JavaScript, with final design and validation decisions made manually.

---

## Getting Started

### Prerequisites

- Python 3.11+
- pip
- (Optional) Docker Desktop

### Installation (Local)

1. Clone the repo
   ```bash
   git clone https://github.com/lefkovitzj/WDW_Transit_Optimizer.git
   cd WDW_Transit_Optimizer
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment
   - Copy [.env.example](.env.example) to `.env`
   - Ensure `GRAPH_DATA_PATH` points to your graph JSON (for example: `data/wdw_graph.json`)

5. (Optional) Regenerate graph data
   ```bash
   python data_converter.py
   ```

6. Run the app
   ```bash
   python -m app.main
   ```
   Or:
   ```bash
   uvicorn app.main:app --reload
   ```

### Run with Docker

Use:
- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)

```bash
docker compose up --build
```

---

## Usage

1. Open the app at `http://127.0.0.1:8000`
2. Choose:
   - Starting point
   - Optional intermediate stops
   - Final destination
3. Submit to receive:
   - Optimized stop order
   - Full stitched itinerary with transit modes
   - Estimated total travel time

Relevant UI templates:
- [app/templates/index.html](app/templates/index.html)
- [app/templates/components/itinerary.html](app/templates/components/itinerary.html)

Graph visualization:
- [app/templates/graph.html](app/templates/graph.html)
- [app/static/js/graph.js](app/static/js/graph.js)

---

## Project Structure

```text
app/
  core/
    config.py
    graph.py
  static/js/
    graph.js
  templates/
    base.html
    graph.html
    index.html
    components/
      itinerary.html
      search_results.html
  main.py
  routes.py
data/
  wdw_graph.json
data_converter.py
database.py
test_optimizer.py
```

---

## Roadmap

- [ ] Add automated tests for route-planning endpoints
- [ ] Add graph validation checks in CI
- [ ] Add transit-time profiles by day/time
- [ ] Improve disconnected-node diagnostics in graph view

---

## Contributing

Contributions are welcome.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourFeature`)
3. Commit your Changes (`git commit -m "feat: add YourFeature"`)
4. Push to the Branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## Contact

Joseph Lefkovitz  
GitHub: [@lefkovitzj](https://github.com/lefkovitzj)  
Project Link: https://github.com/lefkovitzj/WDW_Transit_Optimizer

---

## Acknowledgments

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- Allears.net for articles on Disney transit options and approximate times
- FastAPI + HTMX ecosystem

---

<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white
[python-url]: https://www.python.org/
[fastapi-shield]: https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[htmx-shield]: https://img.shields.io/badge/HTMX-1.9+-3366CC
[htmx-url]: https://htmx.org/
[docker-shield]: https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white
[docker-url]: https://www.docker.com/