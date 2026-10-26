import bpy, math, struct, json, sys
from mathutils import Vector, Matrix
from pathlib import Path
# Usage: blender --background --factory-startup -t 4 --python scripts/export-winter-decor.py -- /path/to/MARC_FINAL.blend
source=sys.argv[sys.argv.index('--')+1]
with bpy.data.libraries.load(source, link=False) as (src,dst):
 dst.objects=[n for n in src.objects if (n.startswith('MK_snowman_') and '/' not in n) or n=='V19 / embedded crest crystal 00 / branched hexagonal ice core']
for ob in dst.objects: bpy.context.scene.collection.objects.link(ob)
out=Path(__file__).resolve().parents[1]/'img/models';out.mkdir(parents=True,exist_ok=True)
deps=bpy.context.evaluated_depsgraph_get()
for name in ['snowman','crystal']:
 objects=[o for o in bpy.context.scene.objects if (o.name.startswith('MK_snowman_') if name=='snowman' else 'branched hexagonal ice core' in o.name)]
 tris=[]
 for ob in objects:
  ev=ob.evaluated_get(deps);mesh=ev.to_mesh();mesh.calc_loop_triangles()
  col=(.9,.96,1)
  if name=='crystal':col=(.56,.78,.96)
  elif 'scarf' in ob.name or 'fringe' in ob.name:col=(.12,.33,.53)
  elif 'twig' in ob.name or 'arm' in ob.name:col=(.30,.23,.19)
  elif 'eye' in ob.name or 'mouth' in ob.name or 'button' in ob.name:col=(.08,.13,.19)
  elif 'nose' in ob.name:col=(.88,.45,.19)
  matrix=ob.matrix_world if name=='snowman' else Matrix.Identity(4)
  normalmat=matrix.to_3x3().inverted().transposed()
  for tri in mesh.loop_triangles:
   pts=[]
   for vi in tri.vertices:
    p=matrix@mesh.vertices[vi].co
    n=(normalmat@(mesh.vertices[vi].normal if mesh.polygons[tri.polygon_index].use_smooth else tri.normal)).normalized()
    if name=='snowman':p=Vector((p.x,p.z,-p.y));n=Vector((n.x,n.z,-n.y))
    pts.append((p,n,col))
   tris.append(pts)
  ev.to_mesh_clear()
 lo=Vector(tuple(min(p[k] for t in tris for p,n,c in t) for k in range(3)));hi=Vector(tuple(max(p[k] for t in tris for p,n,c in t) for k in range(3)))
 center=(lo+hi)*.5;scale=1.7/max(hi-lo)
 vertices=[];indices=[];lookup={}
 for tri in tris:
  for p,n,c in tri:
   p=(p-center)*scale
   key=tuple(round(x,5) for x in (*p,*n,*c))
   if key not in lookup:lookup[key]=len(vertices);vertices.append(key)
   indices.append(lookup[key])
 assert len(vertices)<65536
 with (out/(name+'.bin')).open('wb') as f:
  f.write(struct.pack('<II',len(vertices),len(indices)))
  for v in vertices:f.write(struct.pack('<6h3Bx',*[round(max(-1,min(1,x))*32767) for x in v[:6]],*[round(x*255) for x in v[6:]]))
  f.write(struct.pack('<'+'H'*len(indices),*indices))
 print(name,'vertices',len(vertices),'triangles',len(indices)//3,'bounds',list(lo),list(hi),'bytes',(out/(name+'.bin')).stat().st_size)
