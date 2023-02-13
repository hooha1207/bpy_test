import bpy
import bmesh
import math


#bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

actOb = bpy.context.object
org_co = bpy.context.object.matrix_world.to_translation()
actOb_sc = bpy.context.object.matrix_world.to_scale()
actOb_rt = bpy.context.object.matrix_world.to_euler()

vertList = [((actOb_sc*vertex.co) + org_co) for vertex in actOb.data.vertices if vertex.select]
vertList_idx = [vertex.index for vertex in actOb.data.vertices if vertex.select]

#oa = bpy.context.active_object




obj = bpy.context.object
me = obj.data
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(me)
vertices= [e for e in bm.verts]

#vertices_idx= [e.index for e in bm.verts]
#vertices_co= [((actOb_sc * e.co) + org_co) for e in bm.verts]

vertices_idx_s= [e.index for e in bm.verts if e.select]
vertices_co_s= [((actOb_sc * e.co) + org_co) for e in bm.verts if e.select]


#index = 5 # here the index you want select please change 
#for vert in vertices:
#    if vert.index == index:
#        vert.select = True
#    else:
#        vert.select = False

bmesh.update_edit_mesh(me)
bpy.ops.object.mode_set(mode='OBJECT')






add_amarture_name = "shape_to_amarture"
bone_size = 0.08
rebatch = -(0.5-bone_size/2)

bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0,0,0), scale=(0.01, 0.01, 0.01))
bpy.context.object.name = add_amarture_name

del add_amarture_name

add_amarture_name = bpy.context.object.name

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.armature.select_all(action='SELECT')
bpy.ops.armature.delete()

for idx, i in enumerate(vertices_co_s):
    add_bone_name = f"shape_to_bone{idx}"
    bpy.ops.armature.bone_primitive_add(name=add_bone_name)
    bpy.ops.armature.select_linked()
    bpy.ops.transform.translate(value=i) #world_space_coordinate
    bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
    bpy.ops.transform.translate(value=(0.0,0.0,rebatch))

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = actOb
    
    vertex_idx = [vertices_idx_s[idx]]
    v_group = bpy.context.object.vertex_groups.new(name=add_bone_name) #be wary of vertex group has no duplicate
    v_group.add(vertex_idx, 1.0, "REPLACE")
    
    bpy.context.view_layer.objects.active = bpy.context.scene.objects.get(add_amarture_name)
    bpy.ops.object.mode_set(mode='EDIT')


bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.view_layer.objects.active = actOb
bpy.ops.object.modifier_add(type='ARMATURE')
bpy.context.object.modifiers["Armature"].object = bpy.data.objects[add_amarture_name]
bpy.context.view_layer.objects.active = bpy.context.scene.objects.get(add_amarture_name)


#만약 bone mirror 기능을 만들고 싶다면,
#먼저 대칭되는 객체를 mirror로 만든다 ex) 왼쪽 오른쪽 각각 독립 오브젝트로 만들기
#각각 따로 mesh to bone 스크립트를 실행하고 auto name 기능을 이용해 왼쪽 오른쪽 이름을 만들어준다
#이럼 vertex group 이름에도 대칭이름이 적용된다
#대칭되는 객체 중 하나를 symmetrize 기능으로 생성하고 생성하지 않은 amarture는 삭제한다
#amarture가 삭제된 객체의 amarture를 symmetrize로 반대쪽 bone이 생성된 amarture로 바꿔준다
#mirror 기능으로 bone을 다룰 수 있게 된다
