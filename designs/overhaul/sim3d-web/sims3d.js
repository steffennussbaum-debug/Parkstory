// Photorealistic 3D views for the stacker and the EV charging simulators.
// Each view mirrors its 2D simulator (which keeps the logic, buttons, numbers and texts) and renders it
// with three.js: physically based materials, image-based lighting, soft shadows and filmic tone mapping.
// Build: npx esbuild designs/overhaul/sim3d-web/sims3d.js --bundle --minify --format=iife --outfile=sims3d.min.js
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';

const LIME = 0xb8f03c;
const CELL_X = 2.6;   // pitch across the car (m)
const CELL_Z = 5.6;   // pitch along the car (m)
const LEVEL = 2.15;   // stacker level pitch (m)

function webglOK() {
  try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; }
}

// ---------------------------------------------------------------- textures
function canvasTex(w, h, draw, repeat, srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping;
  if (repeat) t.repeat.set(repeat[0], repeat[1]); if (srgb) t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
function noiseFill(g, w, h, base, amp, n, alpha = 0.5) {
  g.fillStyle = `rgb(${base},${base},${base})`; g.fillRect(0, 0, w, h);
  for (let i = 0; i < n; i++) {
    const v = base + (Math.random() - 0.5) * amp | 0; g.fillStyle = `rgba(${v},${v},${v},${alpha})`;
    const s = Math.random() < 0.08 ? 3 + Math.random() * 6 : 1 + Math.random() * 2; g.fillRect(Math.random() * w, Math.random() * h, s, s);
  }
}
function concrete(repeat) {
  const map = canvasTex(512, 512, (g, w, h) => {
    noiseFill(g, w, h, 172, 30, 30000, 0.3);
    for (let i = 0; i < 40; i++) { // stains
      const x = Math.random() * w, y = Math.random() * h, r = 20 + Math.random() * 90;
      const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, 'rgba(110,110,110,.05)'); gr.addColorStop(1, 'rgba(90,90,90,0)');
      g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r);
    }
  }, repeat);
  const rough = canvasTex(256, 256, (g, w, h) => noiseFill(g, w, h, 205, 60, 9000, 0.6), repeat, false);
  return new THREE.MeshStandardMaterial({ map, roughnessMap: rough, roughness: 0.92, metalness: 0 });
}
function brushed(color, metal, rough, repeat) {
  const map = canvasTex(64, 512, (g, w, h) => {
    g.fillStyle = '#c8c8c8'; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h * 3; y++) { const v = 200 + (Math.random() - 0.5) * 60 | 0; g.fillStyle = `rgba(${v},${v},${v},.5)`; g.fillRect(0, Math.random() * h, w, 1); }
  }, repeat);
  return new THREE.MeshStandardMaterial({ color, map, metalness: metal, roughness: rough });
}
function treadPlate(repeat) { // diamond plate for the conveyor decks
  const map = canvasTex(128, 128, (g, w, h) => {
    g.fillStyle = '#9a9c9e'; g.fillRect(0, 0, w, h);
    for (let y = 0; y < h; y += 16) for (let x = (y / 16) % 2 ? 8 : 0; x < w; x += 16) {
      g.save(); g.translate(x + 4, y + 4); g.rotate(Math.PI / 4); g.fillStyle = '#b9bbbd'; g.fillRect(-1.5, -5, 3, 10); g.fillStyle = '#6d6f72'; g.fillRect(1.5, -5, 1, 10); g.restore();
    }
  }, repeat);
  return new THREE.MeshStandardMaterial({ map, metalness: 0.85, roughness: 0.45 });
}
function labelTex(text, bg, fg) {
  return canvasTex(256, 96, (g, w, h) => {
    g.fillStyle = bg; g.beginPath(); g.roundRect(4, 4, w - 8, h - 8, 44); g.fill();
    g.fillStyle = fg; g.font = '700 46px Inter, Arial, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, w / 2, h / 2 + 2);
  });
}

// ---------------------------------------------------------------- materials
let M = null;
function materials() {
  if (M) return M;
  M = {
    floor: concrete([6, 6]),
    wall: concrete([4, 2]),
    steel: brushed(0xc9ccd0, 0.9, 0.38, [1, 3]),
    galv: brushed(0xb4b8bb, 0.8, 0.5, [1, 2]),
    paint: new THREE.MeshStandardMaterial({ color: 0x2b4a3a, metalness: 0.3, roughness: 0.55 }),
    yellow: new THREE.MeshStandardMaterial({ color: 0xf2b230, metalness: 0.1, roughness: 0.55 }),
    deck: treadPlate([2, 4]),
    roller: new THREE.MeshStandardMaterial({ color: 0xe6a12a, roughness: 0.55 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x141516, roughness: 0.92 }),
    rim: new THREE.MeshStandardMaterial({ color: 0xc9cdd2, metalness: 1, roughness: 0.22 }),
    glass: new THREE.MeshPhysicalMaterial({ color: 0x0b1116, metalness: 0.1, roughness: 0.04, clearcoat: 1, clearcoatRoughness: 0.03 }),
    head: new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfff4d6, emissiveIntensity: 1.2 }),
    tail: new THREE.MeshStandardMaterial({ color: 0x5a0d0d, emissive: 0xc0201a, emissiveIntensity: 0.5 }),
    trim: new THREE.MeshStandardMaterial({ color: 0x1a1c1e, metalness: 0.3, roughness: 0.5 }),
    line: new THREE.MeshStandardMaterial({ color: 0xf0f0ea, roughness: 0.8 }),
    lime: new THREE.MeshStandardMaterial({ color: LIME, emissive: LIME, emissiveIntensity: 0.9, roughness: 0.4 }),
    limeGlow: new THREE.MeshBasicMaterial({ color: LIME, transparent: true, opacity: 0.35, depthWrite: false }),
    cabinGlass: new THREE.MeshPhysicalMaterial({ color: 0xd8f0e0, transparent: true, opacity: 0.18, roughness: 0.05, metalness: 0, clearcoat: 1 }),
    lamp: new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 2.2 }),
  };
  return M;
}
const paints = {};
function paint(hex) {
  if (!paints[hex]) paints[hex] = new THREE.MeshPhysicalMaterial({ color: hex, metalness: 0.55, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.05 });
  return paints[hex];
}
const CAR_COLORS = [0xe9edf0, 0x8e9aa4, 0x2b3033, 0x0e0f11, 0x3c4a5c, 0x6e7580, 0xd9d2c4, 0x1d2c44, 0x7a1d1d, 0xb9bec6, 0x4b5e52];

// ---------------------------------------------------------------- car model (length along Z)
let CARGEO = null;
function carGeometry() {
  if (CARGEO) return CARGEO;
  const L = 4.55, W = 1.82;
  const body = new THREE.Shape();
  body.moveTo(-L / 2, 0.32); body.lineTo(-L / 2 + 0.05, 0.62); body.quadraticCurveTo(-L / 2 + 0.15, 0.82, -L / 2 + 0.55, 0.85);
  body.lineTo(L / 2 - 0.9, 0.88); body.quadraticCurveTo(L / 2 - 0.2, 0.86, L / 2 - 0.05, 0.72); body.lineTo(L / 2, 0.36);
  body.quadraticCurveTo(L / 2, 0.26, L / 2 - 0.15, 0.26); body.lineTo(-L / 2 + 0.15, 0.26); body.quadraticCurveTo(-L / 2, 0.26, -L / 2, 0.32);
  const bodyG = new THREE.ExtrudeGeometry(body, { depth: W - 0.16, bevelEnabled: true, bevelThickness: 0.08, bevelSize: 0.07, bevelSegments: 4, curveSegments: 16 });
  bodyG.translate(0, 0, -(W - 0.16) / 2);
  const cab = new THREE.Shape();
  cab.moveTo(-L / 2 + 0.7, 0.86); cab.quadraticCurveTo(-L / 2 + 1.05, 1.36, -L / 2 + 1.55, 1.4); cab.lineTo(L / 2 - 1.75, 1.42);
  cab.quadraticCurveTo(L / 2 - 1.25, 1.38, L / 2 - 0.95, 0.88); cab.lineTo(-L / 2 + 0.7, 0.86);
  const cabG = new THREE.ExtrudeGeometry(cab, { depth: W - 0.42, bevelEnabled: true, bevelThickness: 0.05, bevelSize: 0.05, bevelSegments: 3, curveSegments: 14 });
  cabG.translate(0, 0, -(W - 0.42) / 2);
  const roof = new THREE.Shape();
  roof.moveTo(-L / 2 + 1.4, 1.37); roof.lineTo(L / 2 - 1.85, 1.39); roof.lineTo(L / 2 - 1.85, 1.45); roof.quadraticCurveTo(-0.2, 1.47, -L / 2 + 1.4, 1.43);
  const roofG = new THREE.ExtrudeGeometry(roof, { depth: W - 0.5, bevelEnabled: true, bevelThickness: 0.03, bevelSize: 0.03, bevelSegments: 2 });
  roofG.translate(0, 0, -(W - 0.5) / 2);
  CARGEO = { L, W, bodyG, cabG, roofG, tyre: new THREE.CylinderGeometry(0.33, 0.33, 0.23, 28), rim: new THREE.CylinderGeometry(0.21, 0.21, 0.235, 16),
    lamp: new THREE.BoxGeometry(0.06, 0.08, 0.32), tailG: new THREE.BoxGeometry(0.05, 0.07, 0.36), grille: new THREE.BoxGeometry(0.05, 0.14, 0.7),
    shadow: new THREE.PlaneGeometry(2.1, 4.8) };
  return CARGEO;
}
let SHADOWTEX = null;
function makeCar(hex) {
  const m = materials(), G = carGeometry(), outer = new THREE.Group(), car = new THREE.Group(), p = paint(hex);
  const add = (geo, mat, cast = true) => { const o = new THREE.Mesh(geo, mat); o.castShadow = cast; o.receiveShadow = true; car.add(o); return o; };
  add(G.bodyG, p); add(G.cabG, m.glass); add(G.roofG, p);
  for (const [x, z] of [[G.L / 2 - 0.82, G.W / 2 - 0.1], [G.L / 2 - 0.82, -G.W / 2 + 0.1], [-G.L / 2 + 0.78, G.W / 2 - 0.1], [-G.L / 2 + 0.78, -G.W / 2 + 0.1]]) {
    const t = add(G.tyre, m.rubber); t.rotation.x = Math.PI / 2; t.position.set(x, 0.33, z);
    const r = add(G.rim, m.rim, false); r.rotation.x = Math.PI / 2; r.position.set(x, 0.33, z);
  }
  for (const z of [G.W / 2 - 0.3, -G.W / 2 + 0.3]) {
    const h = add(G.lamp, m.head, false); h.position.set(G.L / 2 - 0.02, 0.7, z);
    const t = add(G.tailG, m.tail, false); t.position.set(-G.L / 2 + 0.01, 0.74, z);
  }
  const gr = add(G.grille, m.trim, false); gr.position.set(G.L / 2 + 0.01, 0.5, 0);
  car.rotation.y = -Math.PI / 2; // nose towards +Z
  outer.add(car);
  // soft contact shadow, so cars sit on the deck even where the shadow map is coarse
  if (!SHADOWTEX) SHADOWTEX = canvasTex(64, 128, (g, w, h) => { const gr2 = g.createRadialGradient(w / 2, h / 2, 4, w / 2, h / 2, h / 2); gr2.addColorStop(0, 'rgba(0,0,0,.55)'); gr2.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr2; g.fillRect(0, 0, w, h); }, null, false);
  const sh = new THREE.Mesh(G.shadow, new THREE.MeshBasicMaterial({ map: SHADOWTEX, transparent: true, depthWrite: false, opacity: 0.8 }));
  sh.rotation.x = -Math.PI / 2; sh.position.y = 0.01; outer.add(sh);
  outer.userData.paint = p;
  return outer;
}

// ---------------------------------------------------------------- conveyor module (one parking position)
let CONVGEO = null;
function makeConveyor() {
  const m = materials(), g = new THREE.Group(), w = CELL_X - 0.08, d = CELL_Z - 0.08;
  if (!CONVGEO) CONVGEO = { frame: new THREE.BoxGeometry(w, 0.16, d), deck: new THREE.BoxGeometry(w * 0.28, 0.03, d - 0.1), roll: new THREE.CylinderGeometry(0.1, 0.1, 0.07, 16) };
  const frame = new THREE.Mesh(CONVGEO.frame, m.galv); frame.position.y = 0.08; frame.castShadow = frame.receiveShadow = true; g.add(frame);
  for (const x of [-w * 0.33, 0, w * 0.33]) { const dk = new THREE.Mesh(CONVGEO.deck, m.deck); dk.position.set(x, 0.175, 0); dk.receiveShadow = true; g.add(dk); }
  const rolls = new THREE.Group(); g.add(rolls);
  for (const x of [-w * 0.18, w * 0.18]) for (let i = 0; i < 9; i++) {
    const r = new THREE.Mesh(CONVGEO.roll, m.roller); r.rotation.z = Math.PI / 2; r.position.set(x, 0.2, -d / 2 + 0.35 + i * (d - 0.7) / 8); rolls.add(r);
  }
  g.userData.rolls = rolls;
  return g;
}

// ---------------------------------------------------------------- shared scene, camera, controls
class View {
  constructor(host, opts) {
    this.host = host; this.opts = opts;
    const coarse = matchMedia('(any-pointer:coarse)').matches || innerWidth < 700;
    const r = this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    r.outputColorSpace = THREE.SRGBColorSpace; r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = opts.exposure || 1.0;
    r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
    r.setPixelRatio(Math.min(devicePixelRatio || 1, coarse ? 1.5 : 2));
    r.domElement.className = 'p3-canvas'; host.appendChild(r.domElement);
    const sc = this.scene = new THREE.Scene();
    sc.background = new THREE.Color(opts.bg || 0xc9c6bf); sc.fog = new THREE.Fog(sc.background, 60, 140);
    const pm = new THREE.PMREMGenerator(r); sc.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture; sc.environmentIntensity = opts.env || 0.7;
    sc.add(new THREE.HemisphereLight(0xf4f1ea, 0x8d8a83, 0.45));
    const sun = this.sun = new THREE.DirectionalLight(0xfff4e2, opts.sun || 2.6);
    sun.castShadow = true; sun.shadow.mapSize.set(coarse ? 1024 : 2048, coarse ? 1024 : 2048);
    sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.03; sun.shadow.radius = 5; sc.add(sun); sc.add(sun.target);
    const fill = new THREE.DirectionalLight(0xdde6ff, 0.35); fill.position.set(20, 14, -12); sc.add(fill);
    this.camera = new THREE.PerspectiveCamera(32, 1.4, 0.5, 300);
    this.yaw = opts.yaw ?? -0.55; this.pitch = opts.pitch ?? 0.7; this.zoom = 1; this.size = 20; this.target = new THREE.Vector3();
    this.dirty = true; this.visible = true; this.last = performance.now();
    new ResizeObserver(() => this.resize()).observe(host);
    new IntersectionObserver(e => { this.visible = e[0].isIntersecting; }).observe(host);
    this.controls(); this.resize();
    const loop = t => { requestAnimationFrame(loop); if (!this.visible || !host.clientWidth) return; const dt = Math.min(0.1, (t - this.last) / 1000); this.last = t;
      if (this.tick(dt) || this.dirty) { r.render(sc, this.camera); this.dirty = false; } };
    requestAnimationFrame(loop);
  }
  fit(size, target) {
    this.size = size; this.target.copy(target);
    const s = this.sun; s.position.set(target.x - size * 0.7, size * 1.4, target.z + size * 0.6); s.target.position.copy(target);
    const c = s.shadow.camera; c.left = c.bottom = -size * 0.75; c.right = c.top = size * 0.75; c.near = 1; c.far = size * 4; c.updateProjectionMatrix();
    this.resize();
  }
  resize() {
    const w = this.host.clientWidth, h = this.host.clientHeight; if (!w || !h) return;
    this.renderer.setSize(w, h, false); const cam = this.camera; cam.aspect = w / h;
    const half = THREE.MathUtils.degToRad(cam.fov) / 2, hfov = Math.atan(Math.tan(half) * cam.aspect);
    const dist = (this.size / 2) / Math.sin(Math.min(half, hfov)) * 0.95 * this.zoom;
    cam.position.set(this.target.x + Math.sin(this.yaw) * Math.cos(this.pitch) * dist, this.target.y + Math.sin(this.pitch) * dist, this.target.z + Math.cos(this.yaw) * Math.cos(this.pitch) * dist);
    cam.lookAt(this.target); cam.updateProjectionMatrix(); this.dirty = true;
  }
  controls() {
    const el = this.renderer.domElement; let drag = null;
    const ray = new THREE.Raycaster(), v = new THREE.Vector2();
    const pick = e => { if (!this.pickables) return null; const b = el.getBoundingClientRect(); v.set((e.clientX - b.left) / b.width * 2 - 1, -((e.clientY - b.top) / b.height) * 2 + 1);
      ray.setFromCamera(v, this.camera); const hit = ray.intersectObjects(this.pickables(), true)[0]; let o = hit && hit.object; while (o && !o.userData.pick) o = o.parent; return o ? o.userData.pick : null; };
    el.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY, yaw: this.yaw, pitch: this.pitch, moved: false }; });
    el.addEventListener('pointermove', e => {
      if (!drag) { const p = pick(e); el.style.cursor = p ? 'pointer' : 'grab'; return; }
      const dx = e.clientX - drag.x, dy = e.clientY - drag.y; if (Math.abs(dx) + Math.abs(dy) > 5) { drag.moved = true; el.setPointerCapture(e.pointerId); }
      if (drag.moved) { this.yaw = Math.max(-1.3, Math.min(1.0, drag.yaw - dx * 0.005)); this.pitch = Math.max(0.3, Math.min(1.3, drag.pitch + dy * 0.004)); this.resize(); }
    });
    el.addEventListener('pointerup', e => { const d = drag; drag = null; if (d && !d.moved) { const p = pick(e); if (p) p(); } });
    el.addEventListener('pointercancel', () => { drag = null; });
    el.style.touchAction = 'pan-y';
  }
  ground(w, d, extra = 8) {
    const m = materials(), f = new THREE.Mesh(new THREE.BoxGeometry(w + extra * 2, 0.4, d + extra * 2), m.floor);
    f.position.y = -0.2; f.receiveShadow = true; this.scene.add(f); return f;
  }
}

// ---------------------------------------------------------------- toggle 3D / 2D (same as the "pick a car" simulator)
function toggle(host, on3d, onChange) {
  const t = document.createElement('div'); t.className = 's3-toggle p3-toggle'; t.setAttribute('role', 'group'); t.setAttribute('aria-label', 'View');
  t.innerHTML = '<button type="button" data-v="3d" class="on">3D</button><button type="button" data-v="2d">2D</button>';
  host.appendChild(t);
  t.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const is3 = b.dataset.v === '3d';
    t.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); onChange(is3); });
}

// ================================================================ STACKERS
function stackerView() {
  const card = document.getElementById('sim-stacker'), svg = document.getElementById('zSvg'), Z = window.__zsim;
  if (!card || !svg || !Z) return;
  const host = document.createElement('div'); host.className = 'p3-host p3-stack';
  svg.parentNode.insertBefore(host, svg); host.appendChild(svg);
  const view = new View(host, { bg: 0xc4c1ba, yaw: -0.62, pitch: 0.62, exposure: 1.0 });
  const m = materials(), sc = view.scene, C = Z.C, R = Z.R, GC = Z.GC;
  const X = c => (c - (C - 1) / 2) * CELL_X, Zp = r => (r - (R - 1) / 2) * CELL_Z;
  view.ground(C * CELL_X, (R + 1) * CELL_Z);
  // building: back wall, side wall, columns, ceiling lights
  const wall = new THREE.Mesh(new THREE.BoxGeometry(C * CELL_X + 6, 11, 0.3), m.wall); wall.position.set(0, 5.5, Zp(0) - CELL_Z / 2 - 2.2); wall.receiveShadow = true; sc.add(wall);
  // transport level conveyors + transfer cabin
  const conv = {};
  for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) { const k = makeConveyor(); k.position.set(X(c), 0, Zp(r)); sc.add(k); conv[c + ',' + r] = k; }
  const gate = makeConveyor(); gate.position.set(X(GC), 0, Zp(R)); sc.add(gate);
  const cabin = new THREE.Group(), cw = CELL_X - 0.1, cd = CELL_Z - 0.1, chh = 2.4;
  const glass = new THREE.Mesh(new THREE.BoxGeometry(cw, chh, cd), m.cabinGlass); glass.position.y = chh / 2 + 0.02; cabin.add(glass);
  for (const [x, z] of [[-cw / 2, -cd / 2], [cw / 2, -cd / 2], [-cw / 2, cd / 2], [cw / 2, cd / 2]]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.08, chh, 0.08), m.steel); p.position.set(x, chh / 2, z); p.castShadow = true; cabin.add(p); }
  const strip = new THREE.Mesh(new THREE.BoxGeometry(cw - 0.2, 0.03, 0.06), m.lime); strip.position.set(0, chh - 0.06, cd / 2 - 0.06); cabin.add(strip);
  cabin.position.set(X(GC), 0, Zp(R)); sc.add(cabin);
  // driving lane in front of the cabin
  const lane = new THREE.Mesh(new THREE.PlaneGeometry(C * CELL_X + 8, 5), new THREE.MeshStandardMaterial({ color: 0x55575a, roughness: 0.9 }));
  lane.rotation.x = -Math.PI / 2; lane.position.set(0, 0.004, Zp(R) + CELL_Z / 2 + 2.5); lane.receiveShadow = true; sc.add(lane);
  for (let i = -6; i <= 6; i++) { const l = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 0.12), m.line); l.rotation.x = -Math.PI / 2; l.position.set(i * 3, 0.01, Zp(R) + CELL_Z / 2 + 2.5); sc.add(l); }
  const sel = new THREE.Mesh(new THREE.PlaneGeometry(CELL_X - 0.2, CELL_Z - 0.2), m.limeGlow); sel.rotation.x = -Math.PI / 2; sel.visible = false; sc.add(sel);
  const marker = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.7, 4), m.lime); marker.rotation.x = Math.PI; marker.visible = false; sc.add(marker);

  let stackGroup = null, stacksRef = null, S = -1;
  function buildStacks() {
    if (stackGroup) sc.remove(stackGroup);
    stackGroup = new THREE.Group(); sc.add(stackGroup); stacksRef = Z.stacks; S = Z.S;
    const keys = Object.keys(Z.stacks || {}), postG = new THREE.BoxGeometry(0.14, 1, 0.14), trayG = new THREE.BoxGeometry(CELL_X - 0.22, 0.08, CELL_Z - 0.3),
      railG = new THREE.BoxGeometry(0.1, 0.16, CELL_Z - 0.2), beamG = new THREE.BoxGeometry(CELL_X - 0.1, 0.18, 0.12);
    for (const k of keys) {
      const [c, r] = k.split(',').map(Number), x = X(c), z = Zp(r), top = S * LEVEL + 0.9;
      for (const [dx, dz] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
        const p = new THREE.Mesh(postG, m.steel); p.scale.y = top; p.position.set(x + dx * (CELL_X / 2 - 0.1), top / 2, z + dz * (CELL_Z / 2 - 0.1)); p.castShadow = p.receiveShadow = true; stackGroup.add(p);
      }
      for (const dz of [-1, 1]) { const b = new THREE.Mesh(beamG, m.paint); b.position.set(x, top - 0.09, z + dz * (CELL_Z / 2 - 0.1)); b.castShadow = true; stackGroup.add(b); }
      for (const dx of [-1, 1]) { const b = new THREE.Mesh(railG, m.yellow); b.position.set(x + dx * (CELL_X / 2 - 0.1), top - 0.09, z); b.castShadow = true; stackGroup.add(b); }
      for (let j = 1; j <= S; j++) { // storage pallets (move with the car when a level is lowered)
        const t = new THREE.Mesh(trayG, m.galv); t.position.set(x, j * LEVEL + 0.1, z); t.castShadow = t.receiveShadow = true; stackGroup.add(t);
      }
    }
    const h = Math.max(1, S + 1) * LEVEL + 1;
    view.fit(Math.max(C * CELL_X, (R + 1) * CELL_Z) * 0.86 + h * 0.3, new THREE.Vector3(0, h * 0.3, CELL_Z * 0.35));
  }

  const meshes = new Map(); let carsRef = null;
  view.pickables = () => [...meshes.values()].map(o => o.obj);
  const TW = 60, TH = 30, LH = 36;
  function carPos(car) {
    const tr = car.g.getAttribute('transform') || ''; const mm = tr.match(/translate\(([-\d.]+),([-\d.]+)\)/); if (!mm) return null;
    const x = +mm[1], y = +mm[2], tx = (car.c - car.r) * TW / 2;
    if (Math.abs(x - tx) < 0.05) { const z = ((car.c + car.r) * TH / 2 - y) / LH; return [car.c, car.r, z]; } // vertical move or at rest
    const d = x / (TW / 2), s = y / (TH / 2); return [(s + d) / 2, (s - d) / 2, 0];                  // move on the transport level
  }
  view.tick = dt => {
    let moved = false;
    if (Z.stacks !== stacksRef || Z.S !== S) { buildStacks(); moved = true; }
    const cars = Z.cars, seen = new Set();
    for (const car of cars) {
      seen.add(car.id); let o = meshes.get(car.id);
      if (!o) { const obj = makeCar(CAR_COLORS[(car.id * 7 + 3) % CAR_COLORS.length]); obj.userData.pick = () => car.g.dispatchEvent(new MouseEvent('click', { bubbles: true })); sc.add(obj); o = { obj, p: null }; meshes.set(car.id, o); moved = true; }
      const p = carPos(car); if (!p) continue;
      const wx = X(p[0]), wz = Zp(p[1]), wy = 0.21 + p[2] * LEVEL + (p[2] > 0.001 ? 0.07 : 0);
      if (!o.p || Math.abs(o.p[0] - wx) + Math.abs(o.p[1] - wy) + Math.abs(o.p[2] - wz) > 1e-4) { o.obj.position.set(wx, wy, wz); o.p = [wx, wy, wz]; moved = true; }
      const op = parseFloat(car.g.style.opacity || '1'); const vis = op > 0.05; if (o.obj.visible !== vis) { o.obj.visible = vis; moved = true; }
      const hl = car.hl && car.hl.getAttribute('display') !== 'none';
      if (hl) { sel.visible = marker.visible = true; sel.position.set(wx, wy - 0.18, wz); marker.position.set(wx, wy + 2.4 + Math.sin(performance.now() / 260) * 0.12, wz); marker.rotation.y += dt * 1.5; moved = true; o.hl = true; }
      else if (o.hl) { o.hl = false; }
    }
    if (![...meshes.values()].some(o => o.hl)) { if (sel.visible) moved = true; sel.visible = marker.visible = false; }
    for (const [id, o] of meshes) if (!seen.has(id)) { sc.remove(o.obj); meshes.delete(id); moved = true; }
    return moved;
  };
  buildStacks();
  toggle(host, true, is3 => { host.classList.toggle('p3-2d', !is3); if (is3) view.resize(); });
}

// ================================================================ EV CHARGING
function evView() {
  const sim = document.getElementById('sim-ev'), board = document.getElementById('evBoard'); if (!sim || !board) return;
  const wrap = board.parentNode; const host = document.createElement('div'); host.className = 'p3-host p3-ev';
  wrap.parentNode.insertBefore(host, wrap); host.appendChild(wrap);
  const view = new View(host, { bg: 0x1b2026, yaw: -0.38, pitch: 0.78, exposure: 1.05, env: 0.55, sun: 1.6 });
  const m = materials(), sc = view.scene, COLS = 7, ROWS = 4;
  const X = c => (c - (COLS - 1) / 2) * CELL_X, Zp = r => (r - (ROWS - 1) / 2) * CELL_Z;
  view.ground(COLS * CELL_X, ROWS * CELL_Z, 5);
  // a closed garage at night: back wall with the chargers, side walls, ceiling light strips
  const backZ = Zp(0) - CELL_Z / 2 - 0.6;
  const back = new THREE.Mesh(new THREE.BoxGeometry(COLS * CELL_X + 4, 3.4, 0.3), m.wall); back.position.set(0, 1.7, backZ - 0.15); back.receiveShadow = true; sc.add(back);
  const stripe = new THREE.Mesh(new THREE.BoxGeometry(COLS * CELL_X + 4, 0.25, 0.02), new THREE.MeshStandardMaterial({ color: 0x2f7a44, roughness: 0.6 })); stripe.position.set(0, 0.9, backZ + 0.01); sc.add(stripe);
  for (const sx of [-1, 1]) { const w = new THREE.Mesh(new THREE.BoxGeometry(0.3, 3.4, ROWS * CELL_Z + 2), m.wall); w.position.set(sx * (COLS * CELL_X / 2 + 2), 1.7, 0); w.receiveShadow = true; sc.add(w); }
  const lights = new THREE.Group(); sc.add(lights);
  for (let r = 0; r < ROWS; r++) { const l = new THREE.PointLight(0xfff1dc, 9, 14, 1.6); l.position.set(0, 3.2, Zp(r)); lights.add(l);
 }
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) { const k = makeConveyor(); k.position.set(X(c), 0, Zp(r)); sc.add(k); }
  view.fit(Math.max(COLS * CELL_X, ROWS * CELL_Z) * 1.04, new THREE.Vector3(0, 0.6, 0.5));

  // wall chargers
  let chargers = [], chKey = '';
  const chBody = new THREE.BoxGeometry(0.55, 0.8, 0.22), chScr = new THREE.PlaneGeometry(0.3, 0.18);
  function buildChargers(cols) {
    for (const c of chargers) sc.remove(c.g); chargers = [];
    for (const col of cols) {
      const g = new THREE.Group(); g.position.set(X(col), 0, backZ + 0.11);
      const b = new THREE.Mesh(chBody, new THREE.MeshStandardMaterial({ color: 0xf2f3f1, metalness: 0.2, roughness: 0.35 })); b.position.y = 1.35; b.castShadow = true; g.add(b);
      const led = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.04, 0.02), new THREE.MeshStandardMaterial({ color: 0x334, emissive: LIME, emissiveIntensity: 0 })); led.position.set(0, 1.1, 0.12); g.add(led);
      const scr = new THREE.Mesh(chScr, new THREE.MeshStandardMaterial({ color: 0x0b1410, emissive: 0x16351f, emissiveIntensity: 0.6 })); scr.position.set(0, 1.45, 0.112); g.add(scr);
      const glow = new THREE.PointLight(LIME, 0, 3.5, 2); glow.position.set(0, 1.1, 0.6); g.add(glow);
      const cable = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(0, 1.0, 0.12), new THREE.Vector3(0.15, 0.35, 0.5), new THREE.Vector3(0.35, 0.65, 1.15)]), 24, 0.025, 8), m.rubber);
      cable.castShadow = true; g.add(cable);
      sc.add(g); chargers.push({ col, g, led, glow, cable });
    }
  }
  const batt = (k, done) => labelTex(done ? '✓ charged' : Math.round(k) + ' %', done ? '#b8f03c' : 'rgba(7,21,15,.85)', done ? '#07150f' : '#ffffff');
  const meshes = new Map();
  view.tick = dt => {
    let moved = false;
    const cw = [...board.querySelectorAll('.chg-wall')].map(w => Math.round(parseFloat(w.style.left) / (100 / COLS)));
    const key = cw.join(','); if (key !== chKey) { chKey = key; buildChargers(cw); moved = true; }
    const boxes = [...board.querySelectorAll('.chg-box')];
    chargers.forEach((ch, i) => { const on = boxes[i] && boxes[i].classList.contains('on'); const t = on ? 1.2 + Math.sin(performance.now() / 300) * 0.4 : 0;
      if (ch.led.material.emissiveIntensity !== t) { ch.led.material.emissiveIntensity = t; ch.glow.intensity = on ? 2.5 : 0; moved = true; } ch.cable.visible = on; });
    const els = [...board.querySelectorAll('.car')], seen = new Set();
    els.forEach((el, i) => {
      seen.add(el); let o = meshes.get(el);
      const c = parseFloat(el.style.left) / (100 / COLS), r = parseFloat(el.style.top) / (100 / (ROWS + 1)) - 1;
      const tx = X(c), tz = Zp(r);
      if (!o) { const obj = makeCar(CAR_COLORS[(i * 5 + 2) % CAR_COLORS.length]); obj.rotation.y = Math.PI; sc.add(obj);
        const lab = new THREE.Sprite(new THREE.SpriteMaterial({ map: batt(0, false), depthTest: false, transparent: true })); lab.scale.set(2.4, 0.9, 1); lab.position.y = 2.5; lab.renderOrder = 10; obj.add(lab);
        o = { obj, lab, x: tx, z: tz, pct: -1, done: null }; meshes.set(el, o); obj.position.set(tx, 0.21, tz); moved = true; }
      const k = (o.x - tx) ** 2 + (o.z - tz) ** 2;
      if (k > 1e-5) { const f = Math.min(1, dt * 15); o.x += (tx - o.x) * f; o.z += (tz - o.z) * f; o.obj.position.set(o.x, 0.21, o.z); moved = true; }
      const bi = el.querySelector('.batt i'), pct = bi ? Math.round(parseFloat(bi.style.width || '0') / 5) * 5 : 0, done = el.classList.contains('full'), charging = el.classList.contains('charging');
      if (pct !== o.pct || done !== o.done) { o.pct = pct; o.done = done; o.lab.material.map.dispose(); o.lab.material.map = batt(pct, done); o.lab.material.needsUpdate = true; moved = true; }
      const showLab = charging || done || pct > 0; if (o.lab.visible !== showLab) { o.lab.visible = showLab; moved = true; }
    });
    for (const [el, o] of meshes) if (!seen.has(el)) { sc.remove(o.obj); meshes.delete(el); moved = true; }
    return moved;
  };
  toggle(host, true, is3 => { host.classList.toggle('p3-2d', !is3); if (is3) view.resize(); });
}

function start() {
  if (!webglOK()) return;
  try { stackerView(); } catch (e) { console.warn('stacker 3D', e); }
  try { evView(); } catch (e) { console.warn('EV 3D', e); }
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
