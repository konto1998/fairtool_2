function loadStructures() {
  document.querySelectorAll(".structure-viewer").forEach(container => {
    const jsonPath = container.dataset.json;
    if (!jsonPath || container.dataset.loaded === "true") return;

    container.dataset.loaded = "true"; // prevent double init

    fetch(jsonPath)
      .then(r => r.json())
      .then(data => {
        const lattice = data.lattice.matrix;
        const sites = data.sites;

        let xyz = `${sites.length}\nstructure\n`;
        sites.forEach(site => {
          const el = site.element || "X";
          const [x, y, z] = site.xyz;
          xyz += `${el} ${x} ${y} ${z}\n`;
        });

        const viewerContainer = container;
        viewerContainer.style.position = "relative";  // ensures 3Dmol fills it
        viewerContainer.style.width = "100%";
        viewerContainer.style.height = container.style.height || "500px";

        const viewer = $3Dmol.createViewer(viewerContainer);
        viewer.addModel(xyz, "xyz");
        viewer.setStyle({}, { stick: { radius: 0.2 }, sphere: { scale: 0.3 } });

        // === Draw Unit Cell ===
        const [a, b, c] = lattice;
        const v = (v) => ({ x: v[0], y: v[1], z: v[2] });

        const verts = [
          v([0,0,0]), v(a), v(b), v(c),
          v([a[0]+b[0], a[1]+b[1], a[2]+b[2]]),
          v([a[0]+c[0], a[1]+c[1], a[2]+c[2]]),
          v([b[0]+c[0], b[1]+c[1], b[2]+c[2]]),
          v([a[0]+b[0]+c[0], a[1]+b[1]+c[1], a[2]+b[2]+c[2]]),
        ];

        const edges = [[0,1],[0,2],[0,3],[1,4],[1,5],[2,4],[2,6],[3,5],[3,6],[4,7],[5,7],[6,7]];
        edges.forEach(([i,j]) => viewer.addLine({start:verts[i], end:verts[j], color:"black"}));

        viewer.zoomTo();
        viewer.render();
      });
  });
}

// --- Run after full page load (fallback if instant nav disabled) ---
document.addEventListener("DOMContentLoaded", loadStructures);

// --- Run after every Material page navigation ---
if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    loadStructures();
  });
}
