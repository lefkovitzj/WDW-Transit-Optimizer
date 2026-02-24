(async () => {
  try {
    if (!window.vis) throw new Error("vis-network not loaded");

    const res = await fetch("/api/graph");
    if (!res.ok) throw new Error(`/api/graph failed: ${res.status}`);
    const data = await res.json();

    const display = data.display_names || {};
    const idToName = Object.fromEntries(Object.entries(display).map(([name, id]) => [id, name]));
    const conns = data.connections || [];

    const ids = new Set(Object.values(display));
    conns.forEach(c => { ids.add(c.from); ids.add(c.to); });

    const inDeg = new Map(), outDeg = new Map(), adj = new Map();
    for (const id of ids) { inDeg.set(id, 0); outDeg.set(id, 0); adj.set(id, new Set()); }

    for (const c of conns) {
      outDeg.set(c.from, (outDeg.get(c.from) || 0) + 1);
      inDeg.set(c.to, (inDeg.get(c.to) || 0) + 1);
      adj.get(c.from).add(c.to);
      adj.get(c.to).add(c.from);

      if (c.bidirectional) {
        outDeg.set(c.to, (outDeg.get(c.to) || 0) + 1);
        inDeg.set(c.from, (inDeg.get(c.from) || 0) + 1);
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
        for (const nxt of adj.get(cur)) {
          if (!seen.has(nxt)) { seen.add(nxt); stack.push(nxt); }
        }
      }
      components.push(comp);
    }
    components.sort((a, b) => b.length - a.length);
    const largest = new Set(components[0] || []);
    const disconnected = [...ids].filter(id => !largest.has(id));
    const isolated = [...ids].filter(id => (inDeg.get(id) || 0) + (outDeg.get(id) || 0) === 0);

    const isolatedSet = new Set(isolated);
    const disconnectedSet = new Set(disconnected);

    const nodes = [...ids].map(id => ({
      id,
      label: idToName[id] || id,
      title: `${idToName[id] || id}<br/><code>${id}</code>`,
      color: isolatedSet.has(id)
        ? { background: "#fecaca", border: "#dc2626" }
        : disconnectedSet.has(id)
          ? { background: "#fde68a", border: "#d97706" }
          : undefined
    }));

    const edges = conns.map((c, i) => ({
      id: i + 1,
      from: c.from,
      to: c.to,
      arrows: c.bidirectional ? { to: true, from: true } : "to",
      label: c.weight != null ? String(c.weight) : "",
      title: `${c.mode || "Unknown"} (${c.weight ?? "?"} min)`,
      smooth: false
    }));

    const container = document.getElementById("graph");
    const network = new vis.Network(
      container,
      { nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges) },
      {
        autoResize: true,
        interaction: { hover: true, navigationButtons: true, keyboard: true },
        physics: {
          enabled: true,
          stabilization: { enabled: true, iterations: 300 }
        }
      }
    );

    network.once("stabilizationIterationsDone", () => {
      network.fit({ animation: false });
      network.setOptions({ physics: false });
    });

    const stats = document.getElementById("stats");
    const isolatedList = document.getElementById("isolatedList");
    const disconnectedList = document.getElementById("disconnectedList");

    stats.textContent = `Nodes: ${ids.size} | Edges: ${conns.length} | Components: ${components.length} | Largest: ${largest.size}`;

    const toLi = (id) => {
      const li = document.createElement("li");
      li.innerHTML = `${idToName[id] || id}<br/><code>${id}</code>`;
      return li;
    };

    isolated.forEach(id => isolatedList.appendChild(toLi(id)));
    disconnected.forEach(id => disconnectedList.appendChild(toLi(id)));
  } catch (err) {
    console.error(err);
    document.body.innerHTML = `<pre style="padding:12px;">${String(err)}</pre>`;
  }
})();