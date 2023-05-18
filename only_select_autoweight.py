#mesh object를 edit mode에 접근한다
#weight를 적용하고 싶은 mesh를 선택한다
#edti mode를 빠져나와 bone의 pose mode 혹은 edit mode에 접근한다
#선택한 mesh에 weight를 적용하고 싶은 bone을 선택한다

import bpy
import numpy as np

actob = bpy.context.active_object

armature_n = actob.name
mesh_n = [i.name for i in bpy.context.selected_objects if not actob.name == i.name][0]

sel_vert = [i for i in bpy.data.objects[mesh_n].data.vertices if i.select]
sel_bone = [i for i in bpy.data.objects[armature_n].data.bones if i.select]


bv_dic = {}

for bone in sel_bone:
    update = 10000
    vidx = 0
    for vert in sel_vert:
#        bone.length
#        bone.head
#        vert.co
        
        vector = vert.co - bone.head_local
        length = (vector.x**2 + vector.y**2 + vector.z**2)**1/2
#        length = ((vert.co.x - bone.head.x)**2 + (vert.co.y - bone.head.y)**2 + (vert.co.z - bone.head.z)**2)
        
        if length < update:
            update = length
            vidx = vert.index
    
    bv_dic[bone.name] = vidx

for bone_n in bv_dic:
    vgroup = bpy.data.objects[mesh_n].vertex_groups.new(name = bone_n)
    vgroup.add([bv_dic[bone_n]], 1, 'REPLACE')
