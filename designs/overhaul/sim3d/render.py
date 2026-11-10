# python render.py scene.blend variant frames(comma or a-b) outdir pct samples
import bpy, sys, time, addon_utils
addon_utils.enable('cycles', default_set=True)
blend, variant, frames, outdir, pct, samples = sys.argv[-6:]
bpy.ops.wm.open_mainfile(filepath=blend)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = int(samples)
sc.render.resolution_percentage = int(pct)
try: print('sky type', [n.sky_type for n in sc.world.node_tree.nodes if n.type=='TEX_SKY'])
except Exception as e: print(e)
for v in ('v_apt','v_off','v_ret'):
    for c in (v, v+'_light'):
        col = bpy.data.collections.get(c)
        if col: col.hide_render = (v != variant)
if '-' in frames:
    a, b = frames.split('-'); fl = list(range(int(a), int(b)+1))
else: fl = [int(x) for x in frames.split(',')]
for f in fl:
    sc.frame_set(f); sc.render.filepath = '%s/%s_%04d.png' % (outdir, variant, f)
    t = time.time(); bpy.ops.render.render(write_still=True); print('frame', f, round(time.time()-t, 1), 's', flush=True)
