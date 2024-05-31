import bpy


shapeKey_n = 'sign_shapekey'
from_mix = False


base_ob = bpy.context.active_object
target_ob = [i for i in bpy.context.selected_objects if i!=base_ob][0]

if base_ob.data.shape_keys == None:
    base_ob.shape_key_add(name='Basis', from_mix=from_mix)






depsgraph = bpy.context.evaluated_depsgraph_get()
vis_ob = depsgraph.objects[base_ob.name]
target_ob = target_ob.evaluated_get(depsgraph)

sk = base_ob.shape_key_add(name=shapeKey_n, from_mix=from_mix)
skn = sk.name

idx = 0
for v in target_ob.data.vertices:
    sk.data[idx].co = sk.data[idx].co + (v.co - vis_ob.data.vertices[idx].co)
    idx +=1

base_ob.data.shape_keys.key_blocks[skn].value = 1.0
