#pose mode에서 merge 시키고자 하는 bone을 select로 설정한다
#merge 기준이 되는 bone의 경우 active select로 설정한다
#해당 스크립트를 실행한다
import bpy
import numpy as np

bone_delete = False
bone_hide = True
bone_deform = True





print('\n')

actob_n = bpy.context.object.name
selob_n = [i.name for i in bpy.context.selected_objects if not i.name == actob_n]
bpy.ops.object.mode_set(mode='POSE')

hide_bn = []
tmp = []
for pb in bpy.data.objects[actob_n].pose.bones:
    if pb.bone.hide:
        if type(pb.child) == type(None):
            hide_bn.append(pb.name)
            continue
        elif pb.child.bone.hide:
#            tmp.append(pb.name)
            continue
        hide_bn.append(pb.name)
#print(hide_bn)
#print(tmp)

#print(len(hide_bn))
#print(len(tmp))

#print('hide_bn + tmp',len(set(hide_bn + tmp)))

#for i in hide_bn:
#    if not bpy.data.objects[actob_n].pose.bones[i].bone.hide:
#        print('unhide')

#print(hide_bn + tmp)


# must be define hide_parent, and unhide_parent_n
def find_unhide_parent(pb):
    if pb.parent.bone.hide:
        hide_parent.append(pb.parent.name)
        find_unhide_parent(pb.parent)
    elif not pb.parent.bone.hide:
        unhide_parent_n.append(pb.parent.name)
        return

merge_dic = {}
use_bones = []

for hbn in hide_bn:
    hide_parent = [hbn]
    unhide_parent_n = []
    find_unhide_parent(bpy.data.objects[actob_n].pose.bones[hbn])
    use_bones+=hide_parent
    if unhide_parent_n[0] in merge_dic.keys():
        merge_dic[unhide_parent_n[0]] += hide_parent
    else:
        merge_dic[unhide_parent_n[0]] = hide_parent
tmp = []
for i in merge_dic.values():
    tmp+=i


print(merge_dic)
print(len(tmp))

for ob in selob_n:
    for pbn in merge_dic:
        
        vgroup_A_name = pbn
        if type(ob) == type('z'):
            ob = bpy.data.objects[ob]
        vgroup = ob.vertex_groups[vgroup_A_name]
        print('merge_dic[pbn]',merge_dic[pbn])
        for cbn in merge_dic[pbn]:
            print('cnb',cbn)
            vgroup_B_name = cbn
            for id, vert in enumerate(ob.data.vertices):
                available_groups = [v_group_elem.group for v_group_elem in vert.groups]
                A = B = 0.0
                if ob.vertex_groups[vgroup_A_name].index in available_groups:
                    A = ob.vertex_groups[vgroup_A_name].weight(id)
                if ob.vertex_groups[vgroup_B_name].index in available_groups:
                    B = ob.vertex_groups[vgroup_B_name].weight(id)

                # only add to vertex group is weight is > 0
                sum = A + B
                vgroup.add([id], sum ,'REPLACE')
            
            ob.vertex_groups.remove(ob.vertex_groups[cbn])
            
            if not bone_deform:
                bpy.data.objects[actob_n].pose.bones[cbn].bone.use_deform = False
            if bone_hide:
                bpy.data.objects[actob_n].pose.bones[cbn].bone.hide = True
            
            if bone_delete:
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.data.objects[actob_n].data.edit_bones.remove(bpy.data.objects[actob_n].data.edit_bones[cbn])
                bpy.ops.object.mode_set(mode='POSE')
