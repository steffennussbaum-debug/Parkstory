# Builds the "building that could exist" scene in Blender (Cycles). Usage:
#   python scene.py <out.blend>
import bpy, bmesh, math, random, sys, addon_utils
from mathutils import Vector
addon_utils.enable('cycles', default_set=True)
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
W, D = 36.0, 18.0              # footprint (x width, y depth); front face at y=0
GF = 4.0                       # ground floor height
PH = 3.0                       # parking level height
RH = 3.4                       # upper floor height
SL = 0.3                       # slab thickness
P = [GF + i*PH for i in range(4)]          # P1..P4 floor levels
RB = GF + 4*PH                              # first upper floor level (16)
R = [RB + i*RH for i in range(4)]           # R1..R4
TOP = RB + 4*RH                             # roof (29.6)

# ---------------- materials ----------------
def mat(name, color=(0.8,0.8,0.8), rough=0.5, metal=0.0, emit=None, estr=0.0, coat=0.0, obj_color=False, noise=0.0, bump=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes['Principled BSDF']
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if coat: b.inputs['Coat Weight'].default_value = coat; b.inputs['Coat Roughness'].default_value = 0.05
    if obj_color:
        oi = nt.nodes.new('ShaderNodeObjectInfo'); nt.links.new(oi.outputs['Color'], b.inputs['Base Color'])
    elif noise:
        tc = nt.nodes.new('ShaderNodeTexCoord'); nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6; nz.inputs['Detail'].default_value = 8
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color = (*[c*(1-noise) for c in color],1); ramp.color_ramp.elements[1].color = (*[min(1,c*(1+noise)) for c in color],1)
        nt.links.new(nz.outputs['Fac'], ramp.inputs['Fac']); nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
        if bump:
            nz2 = nt.nodes.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 60; nt.links.new(tc.outputs['Object'], nz2.inputs['Vector'])
            bm = nt.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = bump
            nt.links.new(nz2.outputs['Fac'], bm.inputs['Height']); nt.links.new(bm.outputs['Normal'], b.inputs['Normal'])
    else:
        b.inputs['Base Color'].default_value = (*color, 1)
    if emit is not None:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = estr
    return m

def glass_mat(name, tint=(0.75,0.82,0.85), refl=0.12, transp=0.82):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial'); mix = nt.nodes.new('ShaderNodeMixShader')
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); tr.inputs['Color'].default_value = (*tint,1)
    gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.03
    fr = nt.nodes.new('ShaderNodeLayerWeight'); fr.inputs['Blend'].default_value = 0.25
    mth = nt.nodes.new('ShaderNodeMath'); mth.operation = 'MULTIPLY_ADD'; mth.inputs[1].default_value = 1-transp; mth.inputs[2].default_value = refl
    nt.links.new(fr.outputs['Fresnel'], mth.inputs[0]); nt.links.new(mth.outputs[0], mix.inputs['Fac'])
    nt.links.new(tr.outputs[0], mix.inputs[1]); nt.links.new(gl.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], out.inputs['Surface'])
    return m

M = dict(
 concrete = mat('concrete',(0.40,0.395,0.375),0.88,noise=0.22,bump=0.25),
 slabedge = mat('slabedge',(0.46,0.455,0.435),0.85,noise=0.18,bump=0.2),
 floor    = mat('floor',(0.26,0.275,0.285),0.35,noise=0.15),
 asphalt  = mat('asphalt',(0.045,0.045,0.05),0.9,noise=0.25,bump=0.2),
 walk     = mat('walk',(0.55,0.53,0.5),0.8,noise=0.1,bump=0.1),
 paint    = mat('paint',(0.85,0.85,0.82),0.5),
 yellow   = mat('yellow',(0.85,0.62,0.05),0.5),
 frame    = mat('frame',(0.06,0.065,0.07),0.35,metal=0.9),
 glass    = glass_mat('glass'),
 carglass = mat('carglass',(0.02,0.025,0.03),0.05,coat=1.0),
 carpaint = mat('carpaint',(1,1,1),0.3,metal=0.55,coat=1.0,obj_color=True),
 tyre     = mat('tyre',(0.02,0.02,0.02),0.8),
 rim      = mat('rim',(0.6,0.6,0.62),0.25,metal=1.0),
 headl    = mat('headl',(1,1,1),0.1,emit=(1,0.95,0.85),estr=2.0),
 taill    = mat('taill',(0.5,0.02,0.02),0.2,emit=(1,0.05,0.03),estr=1.5),
 garlite  = mat('garlite',(1,1,1),0.5,emit=(0.85,0.92,1.0),estr=16.0),
 warm     = mat('warm',(1,1,1),0.5,emit=(1.0,0.62,0.32),estr=6.0),
 plaster  = mat('plaster',(0.62,0.58,0.53),0.8),
 wood     = mat('wood',(0.42,0.27,0.15),0.55),
 fabric1  = mat('fabric1',(0.55,0.5,0.44),0.9),
 fabric2  = mat('fabric2',(0.2,0.24,0.28),0.9),
 plant    = mat('plant',(0.08,0.25,0.06),0.7),
 conveyor = mat('conveyor',(0.5,0.52,0.54),0.35,metal=0.85),
 convgap  = mat('convgap',(0.03,0.03,0.03),0.6),
 green    = mat('green',(0.35,0.7,0.12),0.4,emit=(0.45,0.85,0.15),estr=1.5),
 highlight= mat('highlight',(1,0.4,0.05),0.6,emit=(1.0,0.38,0.05),estr=0.0),
 screen   = mat('screen',(0.02,0.03,0.05),0.2,emit=(0.5,0.7,1.0),estr=1.2),
 shelf    = mat('shelf',(0.9,0.9,0.88),0.4),
 accent1  = mat('accent1',(0.75,0.18,0.12),0.5),
 accent2  = mat('accent2',(0.12,0.35,0.55),0.5),
 grass    = mat('grass',(0.07,0.16,0.04),0.95,noise=0.3),
)

coll_cache = {}
def coll(name):
    if name not in coll_cache:
        c = bpy.data.collections.new(name); sc.collection.children.link(c); coll_cache[name] = c
    return coll_cache[name]

def box(name, x0, y0, z0, x1, y1, z1, m, c='static', bevel=0.0):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = (v.co.x+0.5)*(x1-x0); v.co.y = (v.co.y+0.5)*(y1-y0); v.co.z = (v.co.z+0.5)*(z1-z0)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = (x0, y0, z0); me.materials.append(M[m] if isinstance(m,str) else m)
    coll(c).objects.link(o)
    if bevel:
        md = o.modifiers.new('bv','BEVEL'); md.width = bevel; md.segments = 2
    return o

# ---------------- site ----------------
box('road', -900, -30, -0.05, 900, -5, 0, 'asphalt')
box('far', -2000, -2000, -0.2, 2000, 2000, -0.06, 'grass')
box('walk', -900, -5, 0, 900, 0, 0.12, 'walk')
box('walk2', -900, -40, 0, 900, -30, 0.12, 'walk')
box('lot', -900, 0, -0.05, 900, 900, 0.02, 'walk')
for i in range(-30, 60, 8): box('lane%d'%i, i, -17.6, 0.001, i+4, -17.4, 0.004, 'paint')
box('curb', -900, -5.2, 0, 900, -5, 0.15, 'walk')
rc = random.Random(3)
citym = [mat('city%d'%k,(g,g*0.98,g*0.95),0.8,noise=0.1) for k,g in enumerate((0.3,0.38,0.46,0.25))]
winm = mat('citywin',(0.05,0.05,0.06),0.2,emit=(1.0,0.7,0.4),estr=1.5)
def cityblock(x0,y0,w,d,h):
    b = box('cb%d_%d'%(x0,y0), x0,y0,0,x0+w,y0+d,h, rc.choice(citym))
    for fl in range(int(h/3.4)):
        if rc.random()<0.55: box('cw%d_%d_%d'%(x0,y0,fl), x0+1, y0-0.05, 1.5+fl*3.4, x0+w-1, y0, 2.6+fl*3.4, winm)
for gx in range(-140, 200, 22):
    for gy in (-75, 40, 70):
        if -10 < gx < 60 and gy == 40: continue
        cityblock(gx + rc.uniform(-3,3), gy + rc.uniform(-3,3), rc.uniform(12,18), rc.uniform(12,20), rc.uniform(9,34))

# ---------------- structure ----------------
def slab(z, name, holes=()):
    # slab at floor level z (top surface = z), with optional rectangular holes (x0,x1,y0,y1)
    if not holes:
        return [box(name, 0, 0, z-SL, W, D, z, 'slabedge')]
    out = []; (hx0,hx1,hy0,hy1) = holes[0]
    out.append(box(name+'a', 0, 0, z-SL, hx0, D, z, 'slabedge'))
    out.append(box(name+'b', hx0, hy1, z-SL, W, D, z, 'slabedge'))
    out.append(box(name+'c', hx1, 0, z-SL, W, hy1, z, 'slabedge')) if hx1 < W else None
    return [o for o in out if o]
RAMP = (24.5, 35.6, 0.6, 5.4)   # ramp footprint in plan
slab(SL, 'gfslab')
for i, z in enumerate(P):
    slab(z, 'pslab%d'%i, holes=[RAMP] if i > 0 else [])
    box('pfloor%d'%i, 0, 0, z, W, D, z+0.01, 'floor')
slab(RB, 'rbslab', holes=[RAMP])
for i, z in enumerate(R[1:]+[TOP]): slab(z, 'rslab%d'%i)
# walls: left, back, right for parking levels; core on the right side
box('wallL', -0.3, 0, GF, 0, D, RB, 'concrete')
box('wallB', 0, D, 0, W, D+0.3, TOP, 'concrete')
box('wallR', W, 0, GF, W+0.3, D, RB, 'concrete')
box('core', W+0.32, 3.5, 0, W+6.8, 14.5, TOP+2.5, 'concrete')
box('annex', W+0.32, -0.4, 0, W+9.5, D+0.3, RB, 'concrete')
box('corewin', W+6.81, 6.5, 2, W+6.86, 11.5, TOP+1.5, 'glass')
for x in (0.0, 9.0, 18.0, 27.0):
    for z0 in P: box('col%d_%d'%(x,z0), x+0.0 if x else 0.0, 11.9, z0, (x or 0.0)+0.5, 12.4, z0+PH-SL, 'concrete')
box('roofpar', -0.2, -0.2, TOP, W+0.2, 0.1, TOP+1.0, 'concrete')
box('roofparL', -0.2, -0.2, TOP, 0.1, D, TOP+1.0, 'concrete')
box('plant1', 6, 8, TOP, 12, 14, TOP+1.6, 'frame'); box('plant2', 20, 9, TOP, 24, 13, TOP+1.2, 'frame')

# ground floor: lobby glass, transfer cabin entrance
box('gfback', 0, 6, SL, W, 6.2, GF-SL, 'plaster')
box('gfwall', 0, 0, SL, 0.3, D, GF, 'concrete')
for x in range(0, 24, 3): box('gfmul%d'%x, x, 0.0, SL, x+0.08, 0.1, GF-SL, 'frame')
box('gfglass', 0, 0.02, SL, 23.8, 0.05, GF-SL, 'glass')
box('lobbylite', 1, 1, GF-SL-0.06, 23, 5, GF-SL-0.02, 'warm')
box('cabin', 24, 0, SL, 35.6, 6.0, GF-SL, 'plaster')
box('cabinin', 25.0, -0.01, SL+0.02, 34.6, 0.02, GF-SL-0.4, mat('cabinlight',(1,1,1),0.3,emit=(0.95,0.97,1.0),estr=3.5))
box('cabinsign', 25.0, -0.03, GF-SL-0.3, 34.6, 0.0, GF-SL-0.05, 'green')

# upper floors: glazing, balconies, warm interiors
def interior_apartment(z, cname, warm_strength=6.0, dense=True, prefix='r'):
    rnd = random.Random(int(z*10))
    for ux in range(5):
        x0 = ux*7.2
        box(prefix+'part%d_%d'%(ux,z), x0+7.1, 0.5, z, x0+7.25, D-0.3, z+RH-SL, 'plaster', c=cname)
        lit = mat('w%s%d_%d'%(prefix,ux,int(z)),(1,1,1),0.5,emit=(1.0,0.7+rnd.random()*0.08,0.42+rnd.random()*0.1),estr=warm_strength*(0.4+rnd.random()*0.9)) if rnd.random()>0.12 else M['plaster']
        box(prefix+'ceil%d_%d'%(ux,z), x0+0.6, 1.5, z+RH-SL-0.04, x0+6.6, 9, z+RH-SL-0.01, lit, c=cname)
        box(prefix+'sofa%d_%d'%(ux,z), x0+1.0, 3.0, z, x0+3.2, 3.9, z+0.75, 'fabric1' if ux%2 else 'fabric2', c=cname, bevel=0.08)
        box(prefix+'table%d_%d'%(ux,z), x0+4.0, 2.5, z+0.72, x0+5.6, 3.5, z+0.78, 'wood', c=cname)
        box(prefix+'tleg%d_%d'%(ux,z), x0+4.7, 2.9, z, x0+4.9, 3.1, z+0.72, 'frame', c=cname)
        box(prefix+'plant%d_%d'%(ux,z), x0+6.2, 1.0, z, x0+6.8, 1.6, z+1.1, 'plant', c=cname, bevel=0.2)
        box(prefix+'back%d_%d'%(ux,z), x0+0.2, 9.0, z, x0+7.0, 9.15, z+RH-SL, 'plaster', c=cname)
def facade(z, cname, prefix='f', balcony=True):
    box(prefix+'glass_%d'%int(z*10), 0.2, 0.25, z, W, 0.3, z+RH-SL, 'glass', c=cname)
    for k in range(0, 21): box(prefix+'mul%d_%d'%(k,int(z*10)), k*1.8, 0.2, z, k*1.8+0.07, 0.32, z+RH-SL, 'frame', c=cname)
    box(prefix+'trans_%d'%int(z*10), 0, 0.2, z+RH-SL-0.12, W, 0.34, z+RH-SL, 'frame', c=cname)
    if balcony:
        for ux in range(5):
            x0 = ux*7.2
            box(prefix+'bal%d_%d'%(ux,int(z*10)), x0+0.6, -1.5, z-0.22, x0+5.4, 0.2, z, 'slabedge', c=cname)
            box(prefix+'rail%d_%d'%(ux,int(z*10)), x0+0.6, -1.5, z, x0+5.4, -1.46, z+1.05, 'glass', c=cname)
            box(prefix+'railtop%d_%d'%(ux,int(z*10)), x0+0.6, -1.52, z+1.03, x0+5.4, -1.44, z+1.07, 'frame', c=cname)
    box(prefix+'glassL_%d'%int(z*10), -0.05, 0.2, z, 0.0, D, z+RH-SL, 'glass', c=cname)
for z in R:
    interior_apartment(z, 'static', warm_strength=5.0); facade(z, 'static')

# ---------------- conventional garage ----------------
for i, z in enumerate(P):
    # ceiling lights
    for yy in (2.8, 9.0, 15.2):
        box('gl%d_%d'%(i,yy), 1.0, yy-0.06, z+PH-SL-0.08, 35.0, yy+0.06, z+PH-SL-0.04, 'garlite', c='garagelights%d'%i)
    # parking lines (front and back rows)
    for k in range(10): box('lnF%d_%d'%(i,k), 0.1+k*2.7, 0.6, z+0.011, 0.2+k*2.7, 5.5, z+0.016, 'paint', c='lines')
    for k in range(9):  box('lnB%d_%d'%(i,k), 0.1+k*2.7, 12.5, z+0.011, 0.2+k*2.7, 17.4, z+0.016, 'paint', c='lines')
    box('hatch%d'%i, 22.5, 12.5, z+0.011, 35.5, 17.4, z+0.016, 'yellow', c='lines')
    # highlight overlays (space only used for driving)
    box('hlA%d'%i, 0.2, 5.6, z+0.02, 35.6, 12.4, z+0.03, 'highlight', c='highlights')
    box('hlB%d'%i, 22.5, 12.5, z+0.02, 35.6, 17.4, z+0.03, 'highlight', c='highlights')
    box('hlC%d'%i, 24.5, 0.6, z+0.02, 35.6, 5.5, z+0.03, 'highlight', c='highlights')
# ramps (one per level, front right), origin at low end so they can shrink
ramp_objs = []
L = RAMP[1]-RAMP[0]; ang = math.atan2(PH, L)
for i, z in enumerate([SL] + P[:3]):
    rise = (GF - SL) if i == 0 else PH
    ang_i = math.atan2(rise, L); Lr = math.hypot(L, rise)
    me = bpy.data.meshes.new('ramp%d'%i); bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    for v in bm.verts: v.co.x = (v.co.x+0.5)*Lr; v.co.y = (v.co.y+0.5)*(RAMP[3]-RAMP[2]); v.co.z = (v.co.z-0.5)*0.25
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('ramp%d'%i, me); me.materials.append(M['slabedge']); coll('ramps').objects.link(o)
    o.location = (RAMP[0], RAMP[2], z); o.rotation_euler = (0, -ang_i, 0); ramp_objs.append(o)
    for k in range(5):
        st = box('rstripe%d_%d'%(i,k), 0, 0, 0, 0.6, 0.12, 0.02, 'paint', c='ramps'); st.parent = o
        st.location = (1.5 + k*2.2, 2.35, 0.125)
# slab fillers that close the ramp openings when ramps go
fillers = []
for i, z in enumerate(P[1:] + [RB]):
    f = box('fill%d'%i, RAMP[0], RAMP[2], z-SL, RAMP[1], RAMP[3], z, 'slabedge', c='fillers'); fillers.append(f)
    f2 = box('fillf%d'%i, RAMP[0], RAMP[2], z, RAMP[1], RAMP[3], z+0.01, 'floor', c='fillers'); f2.parent = f; f2.location = (0,0,SL)
    f.scale = (1, 1, 1)

# ---------------- TilePark conveyors on P1/P2 ----------------
COLS, ROWS, PX, PY = 12, 3, 2.9, 5.9
X0, Y0 = 0.4, 0.3
conv = []
for i in range(2):
    z = P[i]
    for r in range(ROWS):
        for c in range(COLS):
            x0 = X0 + c*PX; y0 = Y0 + r*PY
            pl = box('cv%d_%d_%d'%(i,r,c), x0+0.06, y0+0.06, z, x0+PX-0.06, y0+PY-0.06, z+0.14, 'conveyor', c='conveyors')
            for k in range(6):
                g = box('cvg%d_%d_%d_%d'%(i,r,c,k), 0.1, 0.4+k*0.95, 0.14, PX-0.22, 0.46+k*0.95, 0.147, 'convgap', c='conveyors'); g.parent = pl; g.location = (0.1, 0.4+k*0.95, 0.14)
            led = box('cvl%d_%d_%d'%(i,r,c), 0.05, 0.05, 0.14, 0.25, PY-0.17, 0.15, 'green', c='conveyors'); led.parent = pl; led.location = (0.05, 0.05, 0.14)
            conv.append(pl)

# ---------------- cars ----------------
def make_car_mesh():
    bm = bmesh.new()
    def cube(x0,y0,z0,x1,y1,z1,mi,taper=None):
        r = bmesh.ops.create_cube(bm, size=1)
        vs = r['verts']
        for v in vs:
            v.co.x = x0 + (v.co.x+0.5)*(x1-x0); v.co.y = y0 + (v.co.y+0.5)*(y1-y0); v.co.z = z0 + (v.co.z+0.5)*(z1-z0)
        if taper:
            for v in vs:
                if v.co.z > z0 + (z1-z0)/2:
                    v.co.x = (x0+x1)/2 + (v.co.x-(x0+x1)/2)*taper[0]; v.co.y = taper[2] + (v.co.y-taper[2])*taper[1]
        faces = set(f for v in vs for f in v.link_faces)
        for f in faces: f.material_index = mi
    cube(-0.91, -2.25, 0.30, 0.91, 2.25, 0.98, 0)                 # body
    cube(-0.83, -1.25, 0.98, 0.83, 1.05, 1.44, 1, taper=(0.86, 0.72, -0.2))   # cabin (glass)
    cube(-0.84, -1.10, 1.40, 0.84, 0.85, 1.46, 0, taper=(0.9,0.95,-0.1))       # roof
    cube(-0.80, 2.24, 0.68, -0.45, 2.27, 0.80, 4); cube(0.45, 2.24, 0.68, 0.80, 2.27, 0.80, 4)      # headlights
    cube(-0.85, -2.27, 0.72, -0.40, -2.24, 0.84, 5); cube(0.40, -2.27, 0.72, 0.85, -2.24, 0.84, 5)  # tail lights
    for sx in (-0.82, 0.82):
        for sy in (-1.45, 1.45):
            r = bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.34, radius2=0.34, depth=0.24)
            bmesh.ops.rotate(bm, verts=r['verts'], cent=(0,0,0), matrix=__import__('mathutils').Matrix.Rotation(math.pi/2, 3, 'Y'))
            bmesh.ops.translate(bm, verts=r['verts'], vec=(sx, sy, 0.34))
            for f in set(f for v in r['verts'] for f in v.link_faces): f.material_index = 2
            r2 = bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.2, radius2=0.2, depth=0.26)
            bmesh.ops.rotate(bm, verts=r2['verts'], cent=(0,0,0), matrix=__import__('mathutils').Matrix.Rotation(math.pi/2, 3, 'Y'))
            bmesh.ops.translate(bm, verts=r2['verts'], vec=(sx, sy, 0.34))
            for f in set(f for v in r2['verts'] for f in v.link_faces): f.material_index = 3
    me = bpy.data.meshes.new('car'); bm.to_mesh(me); bm.free()
    for m in ('carpaint','carglass','tyre','rim','headl','taill'): me.materials.append(M[m])
    return me
carmesh = make_car_mesh()
car_template = bpy.data.objects.new('cartemplate', carmesh); coll('lib').objects.link(car_template)
bv = car_template.modifiers.new('bv','BEVEL'); bv.width = 0.09; bv.segments = 3; bv.limit_method = 'ANGLE'
bpy.context.view_layer.objects.active = car_template
COLORS = [(0.85,0.86,0.87),(0.9,0.9,0.9),(0.05,0.05,0.06),(0.25,0.27,0.3),(0.5,0.52,0.55),(0.06,0.12,0.32),(0.45,0.04,0.03),(0.7,0.72,0.74),(0.12,0.2,0.16),(0.02,0.02,0.025)]
def new_car(name, cname='cars'):
    o = bpy.data.objects.new(name, carmesh); coll(cname).objects.link(o)
    md = o.modifiers.new('bv','BEVEL'); md.width = 0.09; md.segments = 3; md.limit_method = 'ANGLE'
    c = random.choice(COLORS); o.color = (*c, 1); return o
coll('lib').hide_render = True; coll('lib').hide_viewport = True

# street cars
for k, x in enumerate((-14, -7.5, 6, 41, 48)):
    o = new_car('street%d'%k, 'static'); o.location = (x, -7.2 if k%2 else -12.5, 0.0); o.rotation_euler = (0,0,math.pi/2 if k%2 else -math.pi/2)
o = new_car('cabincar', 'static'); o.location = (29.8, 3.0, SL); o.rotation_euler = (0,0,0)

# conventional positions: per level front 9 (y center 3.05) and back 8 (y center 14.95)
conv_pos = []
for i, z in enumerate(P):
    for k in range(9): conv_pos.append((1.45+k*2.7, 3.05, z, math.pi, i))
    for k in range(8): conv_pos.append((1.45+k*2.7, 14.95, z, 0.0, i))
# TilePark slots: P1/P2, 3 rows x 12 cols, 2 free per level
free = {(0,1,5),(0,0,11),(1,2,3),(1,1,10)}
tp_pos = []
for i in range(2):
    for r in range(ROWS):
        for c in range(COLS):
            if (i,r,c) in free: continue
            tp_pos.append((X0+c*PX+PX/2, Y0+r*PY+PY/2, P[i]+0.14, i, r, c))
assert len(conv_pos) == len(tp_pos) == 68, (len(conv_pos), len(tp_pos))
cars = [new_car('car%02d'%n) for n in range(68)]

# ---------------- variant interiors on the freed floors P3/P4 ----------------
FREED = [P[2], P[3]]
def freed_facade(cname):
    objs = []
    for z in FREED:
        objs.append(box('vglass_%s_%d'%(cname,z), 0.2, 0.25, z, W, 0.3, z+PH-SL, 'glass', c=cname))
        for k in range(0, 21): objs.append(box('vmul_%s_%d_%d'%(cname,k,z), k*1.8, 0.2, z, k*1.8+0.07, 0.32, z+PH-SL, 'frame', c=cname))
    return objs
def apt(cname):
    for z in FREED:
        for ux in range(5):
            x0 = ux*7.2
            box('apart%d_%d'%(ux,z), x0+7.1, 0.5, z, x0+7.25, D-0.3, z+PH-SL, 'plaster', c=cname)
            box('aceil%d_%d'%(ux,z), x0+0.6, 1.5, z+PH-SL-0.05, x0+6.6, 9, z+PH-SL-0.02, 'warm', c=cname+'_light')
            box('asofa%d_%d'%(ux,z), x0+1.0, 3.0, z, x0+3.2, 3.9, z+0.75, 'fabric1' if ux%2 else 'fabric2', c=cname, bevel=0.08)
            box('atable%d_%d'%(ux,z), x0+4.0, 2.4, z+0.72, x0+5.6, 3.4, z+0.78, 'wood', c=cname)
            box('aleg%d_%d'%(ux,z), x0+4.7, 2.8, z, x0+4.9, 3.0, z+0.72, 'frame', c=cname)
            box('abed%d_%d'%(ux,z), x0+1.2, 6.0, z, x0+3.4, 8.2, z+0.55, 'plaster', c=cname, bevel=0.06)
            box('aplant%d_%d'%(ux,z), x0+6.1, 1.0, z, x0+6.7, 1.6, z+1.2, 'plant', c=cname, bevel=0.2)
            box('aback%d_%d'%(ux,z), x0+0.2, 9.5, z, x0+7.0, 9.65, z+PH-SL, 'plaster', c=cname)
    freed_facade(cname)
def off(cname):
    for z in FREED:
        box('ocore%d'%z, 0.2, 12.0, z, W-0.2, 12.2, z+PH-SL, 'plaster', c=cname)
        for row in range(3):
            for k in range(11):
                x = 1.2 + k*3.1; y = 2.0 + row*3.2
                box('odesk%d_%d_%d'%(z,row,k), x, y, z+0.72, x+1.6, y+0.8, z+0.76, 'shelf', c=cname)
                box('oleg%d_%d_%d'%(z,row,k), x+0.7, y+0.3, z, x+0.9, y+0.5, z+0.72, 'frame', c=cname)
                box('oscr%d_%d_%d'%(z,row,k), x+0.5, y+0.55, z+0.76, x+1.1, y+0.6, z+1.15, 'screen', c=cname)
                box('ochr%d_%d_%d'%(z,row,k), x+0.55, y-0.5, z, x+1.05, y-0.05, z+0.9, 'fabric2', c=cname, bevel=0.05)
        for yy in (2.5, 5.7, 8.9):
            box('olite%d_%d'%(z,yy), 0.8, yy-0.15, z+PH-SL-0.05, W-0.8, yy+0.15, z+PH-SL-0.02, mat('ol%d_%d'%(z,yy),(1,1,1),0.5,emit=(1.0,0.9,0.78),estr=6.0), c=cname+'_light')
        box('oplant%d'%z, 34.0, 1.0, z, 34.8, 1.8, z+1.4, 'plant', c=cname, bevel=0.25)
    freed_facade(cname)
def ret(cname):
    for z in FREED:
        for ux in range(4):
            x0 = ux*9.0
            box('rpart%d_%d'%(ux,z), x0+8.9, 0.5, z, x0+9.05, D-0.3, z+PH-SL, 'plaster', c=cname)
            for k in range(3):
                box('rshelf%d_%d_%d'%(ux,z,k), x0+1.0+k*2.6, 4.0, z, x0+2.2+k*2.6, 9.0, z+1.6, 'shelf', c=cname)
                for lv in range(3):
                    box('rgoods%d_%d_%d_%d'%(ux,z,k,lv), x0+1.05+k*2.6, 4.1, z+0.3+lv*0.45, x0+2.15+k*2.6, 8.9, z+0.55+lv*0.45, 'accent1' if (ux+k+lv)%3==0 else ('accent2' if (ux+k+lv)%3==1 else 'wood'), c=cname)
            box('racc%d_%d'%(ux,z), x0+0.3, 0.35, z+PH-SL-0.6, x0+8.6, 0.45, z+PH-SL-0.1, 'accent2' if ux%2 else 'accent1', c=cname)
            box('rlite%d_%d'%(ux,z), x0+0.8, 1.0, z+PH-SL-0.05, x0+8.2, 11, z+PH-SL-0.02, mat('rl%d_%d'%(ux,z),(1,1,1),0.5,emit=(1.0,0.93,0.85),estr=2.4), c=cname+'_light')
            box('rback%d_%d'%(ux,z), x0+0.2, 11.5, z, x0+8.9, 11.65, z+PH-SL, 'plaster', c=cname)
    freed_facade(cname)
apt('v_apt'); off('v_off'); ret('v_ret')

# ---------------- camera, light, world ----------------
cam = bpy.data.cameras.new('cam'); cam.lens = 28; cam.sensor_width = 36
co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
co.location = (-9.0, -33.0, 9.0)
tgt = Vector((18.5, 8.0, 14.2)); dvec = tgt - co.location
co.rotation_euler = dvec.to_track_quat('-Z','Y').to_euler()
sun = bpy.data.lights.new('sun','SUN'); sun.energy = 3.2; sun.color = (1.0, 0.62, 0.36); sun.angle = math.radians(1.2)
so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so); so.rotation_euler = (math.radians(81), 0, math.radians(-42))
world = bpy.data.worlds.new('w'); sc.world = world; world.use_nodes = True; nt = world.node_tree
sky = nt.nodes.new('ShaderNodeTexSky'); sky.sky_type = 'NISHITA' if 'NISHITA' in [e.identifier for e in sky.bl_rna.properties['sky_type'].enum_items] else sky.sky_type
try:
    sky.sun_elevation = math.radians(4); sky.sun_rotation = math.radians(222); sky.sun_disc = False; sky.altitude = 50; sky.air_density = 1.2; sky.dust_density = 2.5
except Exception as e: print('sky', e)
bg = nt.nodes['Background']; bg.inputs['Strength'].default_value = 0.22
nt.links.new(sky.outputs['Color'], bg.inputs['Color'])

# ---------------- render settings ----------------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.cycles.samples = 32; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6; sc.cycles.transparent_max_bounces = 12; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.render.resolution_x = 1280; sc.render.resolution_y = 720; sc.render.resolution_percentage = 100
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast' if 'AgX - Medium High Contrast' in [e.identifier for e in sc.view_settings.bl_rna.properties['look'].enum_items] else 'None'
sc.view_settings.exposure = 0.0
sc.render.use_persistent_data = True
sc.render.fps = 24
sc.render.film_transparent = False

# ================= ANIMATION =================
# seg1 0-24: highlights on, ramps shrink, openings close
# seg2 25-100: highlights off, cars leave, conveyors rise, cars slide in
# seg3 101-160: freed floors are built out (per variant)
def kf(o, path, f, val=None):
    if val is not None:
        if path == 'location': o.location = val
        elif path == 'scale': o.scale = val
        elif path == 'rotation_euler': o.rotation_euler = val
    o.keyframe_insert(data_path=path, frame=f)
def kvis(o, f, visible):
    o.hide_render = not visible; o.keyframe_insert('hide_render', frame=f)
    for fc in (o.animation_data.action.fcurves if hasattr(o.animation_data.action,'fcurves') else []):
        if fc.data_path == 'hide_render':
            for p in fc.keyframe_points: p.interpolation = 'CONSTANT'
def ease_all():
    for a in bpy.data.actions:
        fcs = getattr(a, 'fcurves', None)
        if fcs is None:
            fcs = [fc for layer in a.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
        for fc in fcs:
            for p in fc.keyframe_points:
                p.interpolation = 'CONSTANT' if fc.data_path == 'hide_render' else 'BEZIER'
                p.easing = 'AUTO'

# emission strength animation helper (material node socket)
def kemit(m, f, val):
    s = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']; s.default_value = val; s.keyframe_insert('default_value', frame=f)

# seg1: highlights + ramps
kemit(M['highlight'], 0, 0.0); kemit(M['highlight'], 8, 2.2); kemit(M['highlight'], 24, 2.2); kemit(M['highlight'], 40, 0.0)
for o in coll('highlights').objects:
    kvis(o, 0, False); kvis(o, 1, True); kvis(o, 41, False)
for k, o in enumerate(ramp_objs):
    kf(o, 'scale', 6+k*2, (1,1,1)); kf(o, 'scale', 20+k*2, (0.001,1,1)); kvis(o, 0, True); kvis(o, 21+k*2, False)
for k, f in enumerate(fillers):
    f.location = (RAMP[0], RAMP[2], f.location.z - 1.2); kf(f, 'location', 10+k*2); kvis(f, 0, False); kvis(f, 10+k*2, True)
    f.location = (RAMP[0], RAMP[2], f.location.z + 1.2); kf(f, 'location', 24+k*2)
for o in coll('lines').objects:
    kvis(o, 0, True); kvis(o, 56, False)

# seg2: cars leave (25-70), conveyors rise (45-62), cars slide in (60-100)
order = list(range(68))
for n, car in enumerate(cars):
    x, y, z, rot, lvl = conv_pos[n]
    kvis(car, 0, True)
    car.location = (x, y, z); car.rotation_euler = (0, 0, rot); kf(car, 'location', 0); kf(car, 'rotation_euler', 0)
    start = 25 + (3-lvl)*4 + int((x/36)*-6) + 6 + (0 if y < 9 else 2)
    start = max(25, start)
    kf(car, 'location', start, (x, y, z)); kf(car, 'rotation_euler', start, (0,0,rot))
    kf(car, 'location', start+8, (x, 9.0, z)); kf(car, 'rotation_euler', start+8, (0,0,-math.pi/2))
    kf(car, 'location', start+22, (44.0, 9.0, z))
    kvis(car, start+22, False)
for k, pl in enumerate(conv):
    z = pl.location.z
    pl.location.z = z - 0.2; kf(pl, 'location', 0); kf(pl, 'location', 44 + (k % 36)//3)
    pl.location.z = z; kf(pl, 'location', 52 + (k % 36)//3)
    kvis(pl, 0, False); kvis(pl, 44 + (k % 36)//3, True)
for n, car in enumerate(cars):
    x, y, z, i, r, c = tp_pos[n]
    start = 60 + (COLS-1-c)*0  # computed below
for n, car in enumerate(cars):
    x, y, z, i, r, c = tp_pos[n]
    s = 58 + c*2 + r + i*2
    d = 16 + int((COLS-1-c)*0.9)
    car.location = (44.0, y, z); car.rotation_euler = (0,0,math.pi); kf(car, 'location', s); kf(car, 'rotation_euler', s)
    kvis(car, s, True)
    kf(car, 'location', s+d, (x, y, z)); kf(car, 'rotation_euler', s+d, (0,0,math.pi))
# garage lights on P3/P4 turn off at start of seg3
for i in (2, 3):
    m = bpy.data.materials.new('gl_off%d'%i); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (1,1,1,1); b.inputs['Emission Color'].default_value = (0.85,0.92,1.0,1)
    s = b.inputs['Emission Strength']; s.default_value = 12; s.keyframe_insert('default_value', frame=100); s.default_value = 0; s.keyframe_insert('default_value', frame=112)
    for o in coll('garagelights%d'%i).objects: o.data.materials[0] = m

# seg3: build-out per variant, 101-160
def build_anim(cname):
    objs = list(coll(cname).objects)
    objs.sort(key=lambda o: (o.location.z, o.location.x))
    for k, o in enumerate(objs):
        s = 102 + int(k / max(1, len(objs)) * 34)
        zf = o.location.z
        kvis(o, 0, False); kvis(o, s, True)
        o.scale = (1, 1, 0.001); kf(o, 'scale', s); o.scale = (1, 1, 1); kf(o, 'scale', s+10)
    for o in coll(cname+'_light').objects:
        kvis(o, 0, False); kvis(o, 120, True)
        m = o.data.materials[0]
        if m.name.startswith('warm') and m.users > 1 and not m.get('cp'):
            pass
    # light materials fade in
    seen = set()
    for o in coll(cname+'_light').objects:
        m = o.data.materials[0]
        if m.name in seen: continue
        seen.add(m.name)
        s = m.node_tree.nodes['Principled BSDF'].inputs['Emission Strength']; v = s.default_value or 6.0
        s.default_value = 0; s.keyframe_insert('default_value', frame=120); s.default_value = v; s.keyframe_insert('default_value', frame=140)
# separate warm material for the apartment variant so the residential floors keep theirs
wa = M['warm'].copy(); wa.name = 'warm_apt'; wa.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value = 2.6
for o in coll('v_apt_light').objects: o.data.materials[0] = wa
for v in ('v_apt','v_off','v_ret'): build_anim(v)
ease_all()
sc.frame_start = 0; sc.frame_end = 160
bpy.ops.wm.save_as_mainfile(filepath=sys.argv[-1])
print('saved', sys.argv[-1], 'objects', len(bpy.data.objects))
