# separate bone
#mesh 일부를 선택한다
#선택된 mesh의 vertex group를 추출한다
#추출한 vertex group을 복제한다
#추출된 vertex group에서 선택된 mesh의 weight value를 삭제한다
#복제된 vertex group에서 선택되지 않은 mesh의 weight value를 삭제해
#선택된 mesh만 weight value가 존재하도록 만들어준다

#이후 armature object로 이동해서 기존에 존재하던 bone을 복제한다
#이후 복제된 vertex group의 이름에 맞게 이름을 바꿔준다
#해당 작업을 진행할 때 bone의 순서를 기억해야 된다
#때문에 복제하기 위해 선택한 bone의 이름 또한 저장될 필요가 있다
#dictionary 구조
#{
#기존 vertex group 이름 : [복제된 vertex group 이름, [select_vertex_index], [vertex_weight_value]]
#}


#만약 vertex group에 bone name만 있는 게 아니라
#다른 속성의 vertex group(ex: attribute를 위해 만든 vertex group)이 존재할 경우
#이를 방지하기 위해 bone이 존재하는 armature를 sel로 선택해야만 된다
#mesh에서 vertex group을 추출할 때 armature에 해당 vertex group 이름이 없을 경우 무시하도록 필터링하자

#bone을 복제할 때 추출한 vertex group 이름과 동일한 bone만 복제하자
#please run this script in EDIT mode

import bpy
import bmesh
import math
import mathutils

#current_mode == EDIT

separate_bone_name = 'separate_bone'

actob = bpy.context.active_object
selob = [i for i in bpy.context.selected_objects if i != actob][0]

actob_n = actob.name
selob_n = selob.name

bone_names = [i.name for i in selob.pose.bones]

bm = bmesh.from_edit_mesh(actob.data)
sel_vidx = [i.index for i in bm.verts if i.select]

for vidx in sel_vidx:
    for v_vg in actob.data.vertices[vidx].groups.values():
        v_vg.weight #vertex_group_value
        v_vg.group #vertex_group_idx
        
#bpy.ops.object.mode_set(mode='OBJECT')
# 아직 미완성
