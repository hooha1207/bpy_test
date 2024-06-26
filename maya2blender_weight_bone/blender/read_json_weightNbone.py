import bpy
import bmesh
from mathutils import Vector, Matrix, Quaternion, Euler

import json
import os



"""
info_path 변수에 maya에서 export script로 만든 json이 모여있는 폴더 경로가 부여되었는지 확인한다
해당 스크립트는 해당 경로에 있는 모든 json을 읽기 때문에
    원치 않는 weight도 읽을 수 있기 때문에 필요한 json 이외의 json 파일은 삭제한다
maya에서 weight를 export 할 때 대상이 된 mesh와
    vertex id가 완전히 동일하며 형태도 비슷한 mesh object가
    blender에 존재하는지 확인한다
해당 스크립트를 실행한다
maya에서 deform joint의 world space 정보를 읽어 blender에서 생성한다
이렇게 생성된 pose mode로 접근한 뒤 apply pose해준다

*** 주의사항
가끔 maya에서 읽은 weight 정보가 망가질 때가 있다
이럴 때는 maya에서 mesh를 duplicate 한 뒤,
원래 연결되어있던 skin cluster에 연결하고
copy skin weight paint로 weight 값을 새로운 mesh에 가져온 뒤
해당 mesh를 타겟으로 export script를 실행해서 json을 생성하고 다시 시도하자
"""




info_path = 'C:'+os.environ['HOMEPATH']+'/Desktop/tmp/test'


bn_length = 1.0

bpy.ops.object.select_all(action='DESELECT')


bones_info = [i for i in os.listdir(info_path) if 'bone' in i]
weights_info = [i for i in os.listdir(info_path) if 'weight' in i]


unique_bns = []

for i in range(len(bones_info)):
    f_b = open(f'{info_path}/{bones_info[i]}', 'r')
    
    
    info_b = json.loads(f_b.readline())
    
    namspace = bones_info[i].replace('bone_test_','')
    namspace = namspace.replace('.json','')
    
    armt_name = namspace+'bone'
    n_armt = bpy.data.armatures.new(armt_name)
    n_armt_ob = bpy.data.objects.new(armt_name, n_armt)
    
    bpy.context.scene.collection.objects.link(n_armt_ob)
    
    bpy.context.view_layer.objects.active = n_armt_ob
    
    for bi in info_b:
        if not bi['bn'] in unique_bns:
#            sc = Vector((bi['sc_x'], bi['sc_y'], bi['sc_z']))
            rot = Euler((bi['rot_x'], bi['rot_y'], bi['rot_z']))
            loc = Vector((bi['loc_x'], bi['loc_y'], bi['loc_z']))
            
            bpy.ops.object.mode_set(mode='EDIT')
            neb = n_armt.edit_bones.new(bi['bn'].split('|')[-1])
            neb.length = bn_length
            
            bpy.ops.object.mode_set(mode='POSE')
            n_armt_ob.pose.bones[bi['bn'].split('|')[-1]].rotation_mode = 'XYZ'
            n_armt_ob.pose.bones[bi['bn'].split('|')[-1]].rotation_euler = rot
            n_armt_ob.pose.bones[bi['bn'].split('|')[-1]].location = loc
            
            unique_bns.append(bi['bn'])

    bpy.ops.pose.armature_apply(selected=False)
    
    f_b.close()

try:
    f_b.close()
except:
    pass


for i in range(len(bones_info)):
    f_w = open(f'{info_path}/{weights_info[i]}', 'r')
    
    info_w = json.loads(f_w.readline())
    
    namspace = weights_info[i].replace('weight_test_','')
    namspace = namspace.replace('.json','')
    
    bpy.context.view_layer.objects.active = bpy.data.objects[namspace]
    
    for wi in info_w:
        for bn in unique_bns:
            if bn in list(wi.keys()):
                
                vgn = bn.split('|')[-1]
                weight = wi[bn]
                vid = wi['vid']
                
                if not vgn in [i.name for i in bpy.data.objects[namspace].vertex_groups]:
                    vg = bpy.data.objects[namspace].vertex_groups.new(name=vgn)
                else:
                    vg = bpy.data.objects[namspace].vertex_groups[vgn]
                vg.add([vid], weight,'REPLACE')
#            else:
#                print(list(wi.keys()))
#                print(bn)
    f_w.close()
    
try:
    f_w.close()
except:
    pass


bpy.ops.object.mode_set(mode='OBJECT')
