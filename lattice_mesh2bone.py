import bpy
import bmesh
import math


#bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

actOb = bpy.context.object
org_co = bpy.context.object.matrix_world.to_translation()
actOb_sc = bpy.context.object.matrix_world.to_scale()
actOb_rt = bpy.context.object.matrix_world.to_euler()



if actOb.type == 'LATTICE':
    vertices_co_s = [((actOb_sc*vertex.co) + org_co) for vertex in actOb.data.points if vertex.select]
    vertices_idx_s = range(len(actOb.data.points))

elif actOb.type == 'MESH':
    obj = bpy.context.object
    me = obj.data
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(me)
    vertices= [e for e in bm.verts]

    vertices_idx_s= [e.index for e in bm.verts if e.select]
    vertices_co_s= [((actOb_sc * e.co) + org_co) for e in bm.verts if e.select]

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







