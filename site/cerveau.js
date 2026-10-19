// Cerveau d'un citoyen en 3D : l'architecture réelle 9 → 6 → 3 avec ses biais,
// soit 6 × (9 + 1) + 3 × (6 + 1) = 81 connexions. Aucun poids réel n'est dessiné :
// ils ne sont pas encore exportés. Canvas 2D, sans bibliothèque ni appel extérieur.
(function () {
  const canvas = document.getElementById('cerveau');
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext('2d');
  const COUCHES = [9, 6, 3];
  const RAYONS = [0.78, 0.55, 0.32];
  const X = [-1.05, 0, 1.05];

  // Neurones : position 3D, couche, biais ou non.
  const noeuds = [];
  COUCHES.forEach((n, c) => {
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2;
      noeuds.push({ x: X[c], y: Math.cos(a) * RAYONS[c], z: Math.sin(a) * RAYONS[c], couche: c, biais: false });
    }
    if (c < COUCHES.length - 1) noeuds.push({ x: X[c], y: 0, z: 0, couche: c, biais: true });
  });
  const deLaCouche = c => noeuds.filter(n => n.couche === c);
  const liens = [];
  for (let c = 0; c < COUCHES.length - 1; c++)
    for (const a of deLaCouche(c)) for (const b of deLaCouche(c + 1)) if (!b.biais) liens.push([a, b]);
  // Garde-fou : le dessin doit compter exactement 81 connexions.
  if (liens.length !== 81) console.warn('cerveau.js : ' + liens.length + ' connexions au lieu de 81');

  const reduit = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let angle = 0.6, dpr = 1;

  function taille() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = canvas.clientWidth || 420;
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(w * dpr);
  }

  function projeter(p) {
    const ca = Math.cos(angle), sa = Math.sin(angle);
    const x = p.x * ca + p.z * sa, z = -p.x * sa + p.z * ca;
    const inc = 0.35, ci = Math.cos(inc), si = Math.sin(inc);
    const y = p.y * ci - z * si, z2 = p.y * si + z * ci;
    const f = 3.2 / (3.2 + z2);
    const s = canvas.width * 0.3;
    return { x: canvas.width / 2 + x * s * f, y: canvas.height / 2 + y * s * f, z: z2, f };
  }

  function dessiner() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const P = new Map(noeuds.map(n => [n, projeter(n)]));
    for (const [a, b] of liens) {
      const pa = P.get(a), pb = P.get(b);
      const prof = 1 - ((pa.z + pb.z) / 2 + 1.2) / 2.4;
      ctx.strokeStyle = 'rgba(57, 217, 111, ' + (0.12 + 0.45 * prof).toFixed(3) + ')';
      ctx.lineWidth = dpr * (a.biais ? 0.6 : 0.9);
      if (a.biais) ctx.setLineDash([3 * dpr, 3 * dpr]); else ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(pa.x, pa.y); ctx.lineTo(pb.x, pb.y); ctx.stroke();
    }
    ctx.setLineDash([]);
    const tri = noeuds.slice().sort((a, b) => P.get(b).z - P.get(a).z);
    for (const n of tri) {
      const p = P.get(n), r = (n.biais ? 3.2 : 5.5) * dpr * p.f;
      ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      if (n.biais) { ctx.strokeStyle = '#6dff9c'; ctx.lineWidth = dpr; ctx.stroke(); }
      else {
        ctx.fillStyle = '#6dff9c'; ctx.shadowColor = '#39d96f'; ctx.shadowBlur = 10 * dpr;
        ctx.fill(); ctx.shadowBlur = 0;
      }
    }
  }

  function boucle() {
    angle += 0.004;
    dessiner();
    requestAnimationFrame(boucle);
  }

  taille();
  window.addEventListener('resize', () => { taille(); dessiner(); });
  if (reduit) dessiner(); else requestAnimationFrame(boucle);
})();
