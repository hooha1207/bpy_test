import bpy


shapeKey_n = 'sign_shapekey'
from_mix = False


base_ob = bpy.context.active_object
target_ob = [i for i in bpy.context.selected_objects if i!=base_ob][0]

if base_ob.data.shape_keys == None:
    base_ob.shape_key_add(name='Basis', from_mix=from_mix)






depsgraph = bpy.context.evaluated_depsgraph_get()
vis_ob = depsgraph.objects[base_ob.name]

sk = base_ob.shape_key_add(name=shapeKey_n, from_mix=from_mix)
skn = sk.name

idx = 0
for v in target_ob.data.vertices:
    sk.data[idx].co = sk.data[idx].co + (v.co - vis_ob.data.vertices[idx].co)
    idx +=1

base_ob.data.shape_keys.key_blocks[skn].value = 1.0


### 해당 스크립트로 shapekey를 만들 경우, mesh가 정확하게 맞지 않는 문제가 발생한다
### 때문에 여러 번 실행해서 shapekey를 병합하도록 하자
### 혹은 추후 해당 스크립트에 여러 번 실행하는 코드를 추가하거나

### 추가로 구현해야 되는 기능으로는,
### 제작된 shapekey가 특정 armature가 특정 pose를 취했을 때 활성화 되도록 driver를 만들어주는 기능이 필요하다
