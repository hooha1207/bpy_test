# Never overlap names




import bpy




sbn_head = True # head or tail
tbn_head = True # head or tail

actob_n = bpy.context.active_object.name

shape_to_bone = [i.name for i in bpy.context.selected_pose_bones if not 'hook' in i.name]
#child
target_bone = [i.name for i in bpy.context.selected_pose_bones if 'hook' in i.name]
#parent

bpy.ops.object.mode_set(mode='EDIT')

distance_dic = {}


for sbn in shape_to_bone:
    min_dis = 999999.0
    nearest_b = None
    for tbn in target_bone:
        if tbn_head:
            target = bpy.data.objects[actob_n].data.edit_bones[tbn].head
        elif not tbn_head:
            target = bpy.data.objects[actob_n].data.edit_bones[tbn].tail
        if sbn_head:
            find = bpy.data.objects[actob_n].data.edit_bones[sbn].head
        elif not sbn_head:
            find = bpy.data.objects[actob_n].data.edit_bones[sbn].tail
        distance = ((target[0] - find[0])**2 + (target[1] - find[1])**2 + (target[2] - find[2])**2)**1/2
        if distance <= min_dis:
            min_dis = distance
            nearest_b = tbn
        elif distance == 0:
            min_dis = distance
            nearest_b = tbn
    distance_dic[sbn] = nearest_b


for sbn in distance_dic:
    bpy.data.objects[actob_n].data.edit_bones[sbn].parent = bpy.data.objects[actob_n].data.edit_bones[distance_dic[sbn]]


bpy.ops.object.mode_set(mode='POSE')
