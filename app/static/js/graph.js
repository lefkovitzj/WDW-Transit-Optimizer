(async () => {
  try {
    if (!window.vis || !window.vis.Network || !window.vis.DataSet) {
      throw new Error("vis-network not loaded. Check /static/vendor/vis-network.min.js");
    }

    const res = await fetch("/api/graph");
    if (!res.ok) throw new Error(`/api/graph failed: ${res.status} ${res.statusText}`);
    const data = await res.json();

    const display = data.display_names || {};
    const connections = data.connections || [];

    const idToName = Object.fromEntries(
      Object.entries(display).map(([readable, id]) => [id, readable])
    );

    const ids = new Set(Object.values(display));
    for (const c of connections) {
      if (c?.from) ids.add(c.from);
      if (c?.to) ids.add(c.to);
    }

    const inDeg = new Map();
    const outDeg = new Map();
    const adj = new Map();

    for (const id of ids) {
      inDeg.set(id, 0);
      outDeg.set(id, 0);
      adj.set(id, new Set());
    }

    for (const c of connections) {
      const from = c.from;
      const to = c.to;
      if (!ids.has(from) || !ids.has(to)) continue;

      outDeg.set(from, (outDeg.get(from) || 0) + 1);
      inDeg.set(to, (inDeg.get(to) || 0) + 1);
      adj.get(from).add(to);
      adj.get(to).add(from);

      if (c.bidirectional) {
        outDeg.set(to, (outDeg.get(to) || 0) + 1);
        inDeg.set(from, (inDeg.get(from) || 0) + 1);
      }
    }

    const seen = new Set();
    const components = [];
    for (const id of ids) {
      if (seen.has(id)) continue;
      const comp = [];
      const stack = [id];
      seen.add(id);
      while (stack.length) {
        const cur = stack.pop();
        comp.push(cur);
        for (const nxt of adj.get(cur) || []) {
          if (!seen.has(nxt)) { seen.add(nxt); stack.push(nxt); }
        }
      }
      components.push(comp);
    }

    components.sort((a, b) => b.length - a.length);

    const isolated = [...ids].filter(
      (id) => ((inDeg.get(id) || 0) + (outDeg.get(id) || 0)) === 0
    );
    const isolatedSet = new Set(isolated);

    function edgeColor(mode) {
      const m = String(mode || "").toLowerCase();
      if (m.includes("monorail")) return "#7c3aed";
      if (m.includes("skyliner")) return "#0ea5e9";
      if (m.includes("boat") || m.includes("ferry") || m.includes("launch")) return "#10b981";
      if (m.includes("bus")) return "#f59e0b";
      if (m.includes("walk")) return "#6b7280";
      return "#2563eb";
    }

    function separateOverlappingEdges(edges) {
      const groups = new Map();
      for (const e of edges) {
        const from = String(e.from);
        const to = String(e.to);
        const key = from < to ? `${from}|${to}` : `${to}|${from}`;
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push(e);
      }
      for (const list of groups.values()) {
        if (list.length <= 1) {
          list[0].smooth = false;
          continue;
        }

        for (let i = 0; i < list.length; i++) {
          const layer = i;
          const cw = i % 2 === 0;

          list[i].smooth = {
            enabled: true,
            type: cw ? "curvedCW" : "curvedCCW",
            roundness: 0.24 * layer
          };
        }
      }
      return edges;
    }

    // ---------- Layout helpers ----------
    const LAYOUT_KEY = "wdw_graph_layout_v1";
    const DEFAULT_LAYOUT_URL = "/static/data/graph_layout.json";

    function applySavedPositions(nodes, saved) {
      return nodes.map((n) => {
        const p = saved[String(n.id)];
        if (!p) return n;
        return { ...n, x: p.x, y: p.y };
      });
    }

    function layoutSpread(positions) {
      const vals = Object.values(positions || {});
      if (!vals.length) return 0;
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      for (const p of vals) {
        if (p.x < minX) minX = p.x;
        if (p.x > maxX) maxX = p.x;
        if (p.y < minY) minY = p.y;
        if (p.y > maxY) maxY = p.y;
      }
      return Math.max(maxX - minX, maxY - minY);
    }

    async function loadLayout() {
      try {
        const raw = localStorage.getItem(LAYOUT_KEY);
        if (raw) {
          const parsed = JSON.parse(raw);
          if (Object.keys(parsed).length > 0) return parsed;
        }
      } catch { /* fall through */ }
      try {
        const r = await fetch(DEFAULT_LAYOUT_URL);
        if (r.ok) return await r.json();
      } catch { /* fall through */ }
      return {};
    }

    function saveLayout(network) {
      try {
        const positions = network.getPositions();
        // either remove this guard, or reduce heavily (ex: < 150)
        // if (layoutSpread(positions) < 700) return;
        localStorage.setItem(LAYOUT_KEY, JSON.stringify(positions));
      } catch { /* ignore */ }
    }

    function debounce(fn, wait = 500) {
      let t;
      return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), wait); };
    }

    function downloadLayout(network) {
      const positions = network.getPositions();
      const blob = new Blob([JSON.stringify(positions, null, 2)], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "graph_layout.json";
      a.click();
      URL.revokeObjectURL(a.href);
    }

    function uploadLayout(network, nodeDS) {
      const input = document.createElement("input");
      input.type = "file";
      input.accept = ".json,application/json";
      input.onchange = async () => {
        try {
          const text = await input.files[0].text();
          const layout = JSON.parse(text);
          localStorage.setItem(LAYOUT_KEY, JSON.stringify(layout));
          const updates = Object.entries(layout).map(([id, p]) => ({ id, x: p.x, y: p.y }));
          nodeDS.update(updates);
          network.setOptions({ physics: false });
        } catch {
          alert("Invalid layout JSON file.");
        }
      };
      input.click();
    }

    // ---------- Build nodes/edges ----------
    const nodeItems = [...ids].map((id) => {
      const readable = idToName[id] || id;
      const isIso = isolatedSet.has(id);
      return {
        id,
        label: readable,
        title: `${readable}<br/><code>${id}</code>`,
        shape: "dot",
        size: isIso ? 16 : 11,
        color: isIso ? { background: "#fecaca", border: "#dc2626" } : undefined
      };
    });

    let edgeItems = connections.map((c, i) => ({
      id: i + 1,
      from: c.from,
      to: c.to,
      arrows: c.bidirectional ? { to: true, from: true } : "to",
      label: c.weight != null ? String(c.weight) : "",
      title: `${c.mode || "Unknown"} (${c.weight ?? "?"} min)`,
      color: { color: edgeColor(c.mode) },
      smooth: false
    }));

    edgeItems = separateOverlappingEdges(edgeItems);

    const container = document.getElementById("graph");
    if (!container) throw new Error("Missing #graph element in graph.html");

    // ---------- Load layout + create network ----------
    const savedPositions = await loadLayout();
    const hasSavedLayout = Object.keys(savedPositions).length > 0;

    const nodeDS = new vis.DataSet(applySavedPositions(nodeItems, savedPositions));
    const edgeDS = new vis.DataSet(edgeItems);

    const options = {
      autoResize: true,
      interaction: { hover: true, navigationButtons: true, keyboard: true },
      physics: { enabled: !hasSavedLayout, stabilization: { iterations: 300 } },
      edges: { smooth: false, font: { align: "top" } }
    };

    const network = new vis.Network(container, { nodes: nodeDS, edges: edgeDS }, options);
    window.wdwNetwork = network;

    const debouncedSave = debounce(() => saveLayout(network), 600);
    network.on("dragEnd", debouncedSave);
    network.on("stabilized", debouncedSave);

    if (!hasSavedLayout) {
      network.once("stabilizationIterationsDone", () => {
        network.fit({ animation: false });
        network.setOptions({ physics: false });
        saveLayout(network);
      });
    }

    document.getElementById("btn-download-layout")
      ?.addEventListener("click", () => downloadLayout(network));
    document.getElementById("btn-upload-layout")
      ?.addEventListener("click", () => uploadLayout(network, nodeDS));

    // ---------- Connectivity side panel ----------
    const statsEl = document.getElementById("stats");
    const isolatedListEl = document.getElementById("isolatedList");

    const makeLi = (id) => {
      const li = document.createElement("li");
      li.innerHTML = `${idToName[id] || id}<br/><code>${id}</code>`;
      return li;
    };

    if (statsEl) {
      statsEl.textContent =
        `Nodes: ${ids.size} | Edges: ${connections.length} | Components: ${components.length}`;
    }

    if (isolatedListEl) {
      isolatedListEl.innerHTML = "";
      isolated.forEach((id) => isolatedListEl.appendChild(makeLi(id)));
    }

    // ---------- Search ----------
    const searchInput = document.getElementById("nodeSearch");
    const searchBtn = document.getElementById("searchBtn");
    const clearBtn = document.getElementById("clearSearchBtn");
    const searchStatus = document.getElementById("searchStatus");
    const searchResults = document.getElementById("searchResults");

    const allNodes = nodeDS.get();
    const baseNodeById = new Map(allNodes.map((n) => [n.id, { ...n }]));

    function resetHighlights() {
      nodeDS.update([...baseNodeById.values()].map((n) => ({ ...n })));
      network.unselectAll();
      if (searchStatus) searchStatus.textContent = "";
      if (searchResults) searchResults.innerHTML = "";
    }

    function highlightAndFocus(id) {
      const base = baseNodeById.get(id);
      if (!base) return;
      nodeDS.update([{
        ...base, id, size: 24, borderWidth: 3,
        color: { background: "#fde047", border: "#a16207" }
      }]);
      network.selectNodes([id]);
      network.focus(id, { scale: 1.15, animation: true });
    }

    function runSearch() {
      if (!searchInput) return;
      const q = (searchInput.value || "").trim().toLowerCase();
      resetHighlights();
      if (!q) return;
      const matches = allNodes.filter((n) => {
        const label = String(n.label || "").toLowerCase();
        const id = String(n.id || "").toLowerCase();
        return label.includes(q) || id.includes(q);
      });
      if (!matches.length) {
        if (searchStatus) searchStatus.textContent = "No matches.";
        return;
      }
      if (searchStatus) searchStatus.textContent = `${matches.length} match(es).`;
      highlightAndFocus(matches[0].id);
      if (searchResults) {
        searchResults.innerHTML = "";
        for (const m of matches.slice(0, 50)) {
          const li = document.createElement("li");
          const btn = document.createElement("button");
          btn.type = "button";
          btn.textContent = `${m.label} (${m.id})`;
          btn.addEventListener("click", () => { resetHighlights(); highlightAndFocus(m.id); });
          li.appendChild(btn);
          searchResults.appendChild(li);
        }
      }
    }

    if (searchBtn) searchBtn.addEventListener("click", runSearch);
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        if (searchInput) searchInput.value = "";
        resetHighlights();
      });
    }
    if (searchInput) {
      searchInput.addEventListener("keydown", (e) => { if (e.key === "Enter") runSearch(); });
    }

  } catch (err) {
    console.error(err);
    document.body.innerHTML = `<pre style="padding:12px;white-space:pre-wrap;">${String(err)}</pre>`;
  }
})();