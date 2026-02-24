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

    // Map internal ID -> readable name
    const idToName = Object.fromEntries(
      Object.entries(display).map(([readable, id]) => [id, readable])
    );

    // Include all known nodes + any node found in edges
    const ids = new Set(Object.values(display));
    for (const c of connections) {
      if (c?.from) ids.add(c.from);
      if (c?.to) ids.add(c.to);
    }

    // Degree + undirected adjacency (for connectivity analysis)
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

      // undirected link for connected-components
      adj.get(from).add(to);
      adj.get(to).add(from);

      if (c.bidirectional) {
        outDeg.set(to, (outDeg.get(to) || 0) + 1);
        inDeg.set(from, (inDeg.get(from) || 0) + 1);
      }
    }

    // Connected components (undirected)
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
          if (!seen.has(nxt)) {
            seen.add(nxt);
            stack.push(nxt);
          }
        }
      }
      components.push(comp);
    }

    components.sort((a, b) => b.length - a.length);
    const largestComponent = new Set(components[0] || []);
    const disconnectedFromLargest = [...ids].filter((id) => !largestComponent.has(id));
    const isolated = [...ids].filter((id) => ((inDeg.get(id) || 0) + (outDeg.get(id) || 0)) === 0);

    const isolatedSet = new Set(isolated);
    const disconnectedSet = new Set(disconnectedFromLargest);

    function edgeColor(mode) {
      const m = String(mode || "").toLowerCase();
      if (m.includes("monorail")) return "#7c3aed";
      if (m.includes("skyliner")) return "#0ea5e9";
      if (m.includes("boat") || m.includes("ferry") || m.includes("launch")) return "#10b981";
      if (m.includes("bus")) return "#f59e0b";
      if (m.includes("walk")) return "#6b7280";
      return "#2563eb";
    }

    const nodeItems = [...ids].map((id) => {
      const readable = idToName[id] || id;
      const isIso = isolatedSet.has(id);
      const isDisc = disconnectedSet.has(id);

      return {
        id,
        label: readable,
        title: `${readable}<br/><code>${id}</code>`,
        shape: "dot",
        size: isIso ? 16 : 11,
        color: isIso
          ? { background: "#fecaca", border: "#dc2626" } // isolated = red-ish
          : isDisc
            ? { background: "#fde68a", border: "#d97706" } // disconnected = yellow-ish
            : undefined
      };
    });

    const edgeItems = connections.map((c, i) => ({
      id: i + 1,
      from: c.from,
      to: c.to,
      arrows: c.bidirectional ? { to: true, from: true } : "to",
      label: c.weight != null ? String(c.weight) : "",
      title: `${c.mode || "Unknown"} (${c.weight ?? "?"} min)`,
      color: { color: edgeColor(c.mode) },
      smooth: false
    }));

    const container = document.getElementById("graph");
    if (!container) throw new Error("Missing #graph element in graph.html");

    const nodeDS = new vis.DataSet(nodeItems);
    const edgeDS = new vis.DataSet(edgeItems);

    const network = new vis.Network(
      container,
      { nodes: nodeDS, edges: edgeDS },
      {
        autoResize: true,
        interaction: {
          hover: true,
          navigationButtons: true,
          keyboard: true
        },
        layout: { improvedLayout: true },
        physics: {
          enabled: true,
          stabilization: { enabled: true, iterations: 400 },
          barnesHut: {
            gravitationalConstant: -5000,
            springLength: 140,
            springConstant: 0.04
          }
        },
        edges: { font: { size: 10 } },
        nodes: { font: { size: 12 } }
      }
    );

    network.once("stabilizationIterationsDone", () => {
      network.fit({ animation: false });
      network.setOptions({ physics: false });
    });

    // ---------- Connectivity side panel ----------
    const statsEl = document.getElementById("stats");
    const isolatedListEl = document.getElementById("isolatedList");
    const disconnectedListEl = document.getElementById("disconnectedList");

    const makeLi = (id) => {
      const li = document.createElement("li");
      li.innerHTML = `${idToName[id] || id}<br/><code>${id}</code>`;
      return li;
    };

    if (statsEl) {
      statsEl.textContent =
        `Nodes: ${ids.size} | Edges: ${connections.length} | Components: ${components.length} | Largest: ${largestComponent.size}`;
    }

    if (isolatedListEl) {
      isolatedListEl.innerHTML = "";
      isolated.forEach((id) => isolatedListEl.appendChild(makeLi(id)));
    }

    if (disconnectedListEl) {
      disconnectedListEl.innerHTML = "";
      disconnectedFromLargest.forEach((id) => disconnectedListEl.appendChild(makeLi(id)));
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
        ...base,
        id,
        size: 24,
        borderWidth: 3,
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
          btn.addEventListener("click", () => {
            resetHighlights();
            highlightAndFocus(m.id);
          });
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
      searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") runSearch();
      });
    }

  } catch (err) {
    console.error(err);
    document.body.innerHTML = `<pre style="padding:12px;white-space:pre-wrap;">${String(err)}</pre>`;
  }
})();