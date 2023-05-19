import bpy


perm_vg_name = 'perm'
pos_vg_name = 'pos'






#bpy.ops.object.mode_set(mode='OBJECT')
selOb = bpy.context.selected_objects


selArm = {}
selMesh = {}

bpy.ops.object.select_all(action='DESELECT')

for ob in selOb:
    if "perm" in ob.name:
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='SELECT')
        last_bone = bpy.context.selected_editable_bones[-1]
        
        bpy.ops.armature.select_all(action='DESELECT')
        last_bone.select_tail = True
        
        bpy.ops.armature.extrude_move(ARMATURE_OT_extrude={"forked":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.5)})
        bpy.ops.armature.select_more()
        bpy.ops.armature.parent_clear(type='CLEAR')
        
        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='SELECT')
        ob.data.bones.active = ob.data.bones[bpy.context.selected_pose_bones[-1].name]
        bone = bpy.context.selected_pose_bones[-1]
        bpy.ops.pose.select_all(action='DESELECT')
        cstrt = bone.constraints.new("COPY_LOCATION")
        cstrt.target = bpy.data.objects[ob.name]
        cstrt.subtarget = ob.data.bones[-2].name
        cstrt.head_tail = 1
        bpy.ops.constraint.apply(constraint="Copy Location", owner='BONE')
        
        bpy.ops.pose.select_all(action='DESELECT')
        ob.data.bones.active = ob.data.bones[ob.data.bones[-2].name]
        ob.data.bones[-1].select = True
        bpy.ops.pose.ik_add(with_targets=True)
        
        bpy.ops.object.mode_set(mode='OBJECT')




perm_count = 0
pos_count = 0
card_count = 0


join_perm = None
join_pos = None
join_card = None

perm_l = []
pos_l = []
card_l = []

for ob in selOb:
    if "perm" in ob.name:
        for bone in ob.data.bones.values():
            if 'Bone' in bone.name:
                bone.name = f'{perm_vg_name}_{perm_count}.{bone.name.split(".")[-1]}'
            if perm_count == 0:
                join_perm = ob
            perm_count+=1
        perm_l.append(ob)
                
    elif "pos" in ob.name:
        for bone in ob.data.bones.values():
            bone.name = f'{pos_vg_name}_{pos_count}.{bone.name.split(".")[-1]}'
            if pos_count == 0:
                join_pos = ob
            pos_count+=1
        pos_l.append(ob)
    elif "card" in ob.name:
        card_l.append(ob)
        if card_count == 0:
            join_card = ob
        card_count+=1



c = {}
c["object"] = join_perm
c["active_object"] = join_perm
c["selected_objects"] = perm_l
c["selected_editable_objects"] = perm_l

bpy.ops.object.join(c)


del c

c = {}
c["object"] = join_pos
c["active_object"] = join_pos
c["selected_objects"] = pos_l
c["selected_editable_objects"] = pos_l

bpy.ops.object.join(c)



for ob in card_l:
    if "card" in ob.name:
        ob.modifiers[ob.modifiers.find('perm')].object = bpy.data.objects[join_perm.name]
        ob.modifiers[ob.modifiers.find('pos')].object = bpy.data.objects[join_pos.name]

thickness = {}
re_thickness = join_card.modifiers['Solidify'].thickness

for ob in card_l:
    thickness[ob.name] = ob.modifiers['Solidify'].thickness



for ob in card_l:
    vgroup = ob.vertex_groups['solidify']
    scale = thickness[ob.name] / re_thickness
    for id, vert in enumerate(ob.data.vertices):
        available_groups = [v_group_elem.group for v_group_elem in vert.groups]
        if ob.vertex_groups['solidify'].index in available_groups:
            before = ob.vertex_groups['solidify'].weight(id)
        vgroup.add([id], before*scale, 'REPLACE')


del c

c = {}
c["object"] = join_card
c["active_object"] = join_card
c["selected_objects"] = card_l
c["selected_editable_objects"] = card_l

bpy.ops.object.join(c)
