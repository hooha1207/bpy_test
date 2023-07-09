# 선택한 bone을 for 반복문으로 하나씩 빼서 추출한 bone의 tail location을 구한 뒤,
# 추출한 bone을 제외한 나머지 bone에서 head location을 추출한다
# tail과 head의 location의 distance가 0인 것들끼리 dictionary로 짝을 이뤄준다
# tail bone에 stretch_to constraints를 추가하고 subtarget을 head bone으로 지정한다

import bpy


add_bone_name = 'stretch_n'
constraints_n = 'stretch_target'
bone_size = 0.5

bone_layer = 8





rebatch = -(0.5-bone_size/2)

select_bone_layer = [  ] + [bone_layer]











bpy.ops.object.mode_set(mode='EDIT')

Bbone_layer = []
for i in range(len(bpy.context.object.data.layers)):
    if i in select_bone_layer:
        Bbone_layer.append(True)
    else:
        Bbone_layer.append(False)

rebatch = -(0.5-bone_size/2)

actob_n = bpy.context.active_object.name
selb_n = [i.name for i in bpy.context.selected_editable_bones]


# head_bn : tail_bn
tailhead_dic = {}


for eb1 in selb_n:
    for eb2 in selb_n:
        if bpy.data.objects[actob_n].data.edit_bones[eb1].name != bpy.data.objects[actob_n].data.edit_bones[eb2].name:
            target = bpy.data.objects[actob_n].data.edit_bones[eb1].tail
            find = bpy.data.objects[actob_n].data.edit_bones[eb2].head
            # 만약 nearest_연산에 threshold를 추가하고 싶다면, 해당 부분을 수정하면 된다
            # 하지만, 시도해본 결과 왜인지는 모르겠지만 비교 ㅇ녀산이 정상적으로 수행되지 않는다
            # 이는 추후 수정해보고자 한다
            if ((target[0]-find[0])**2 + (target[1]-find[1])**2 + (target[2]-find[2])**2) ** 1/2 == float(0):
                min_bn = eb2
                print(((target[0]-find[0])**2 + (target[1]-find[1])**2 + (target[2]-find[2])**2) ** 1/2)
                break
            else:
                min_bn = None
    
    tailhead_dic[eb1] = min_bn
#    print(min_bn)
#    print(min_distance)

print(tailhead_dic)

for tailbn in tailhead_dic:
    if tailhead_dic[tailbn] == None:
        continue
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.bone_primitive_add(name=add_bone_name)
    bpy.ops.armature.select_linked()
    check_add_bone_name = bpy.context.selected_editable_bones[0].name
    #set place
    bpy.ops.transform.translate(value=bpy.data.objects[actob_n].data.edit_bones[tailbn].head) #world_space_coordinate
    bpy.ops.transform.resize(value=(bone_size, bone_size, bone_size))
    bpy.ops.transform.translate(value=(0.0,0.0,rebatch))
    
    bpy.ops.object.mode_set(mode='POSE')
    cstrt = bpy.data.objects[actob_n].pose.bones[tailbn].constraints.new("COPY_LOCATION")
    cstrt.target = bpy.data.objects[actob_n]
#    cstrt.subtarget = tailhead_dic[tailbn]
    cstrt.subtarget = check_add_bone_name
    
    tailhead_dic[tailbn] = [tailhead_dic[tailbn], check_add_bone_name]
    
print(tailhead_dic)
#stretch_constraints
for tailbn in tailhead_dic:
    if tailhead_dic[tailbn] != None and tailhead_dic[tailhead_dic[tailbn][0]] != None:
        print(tailbn)
#        print(tailhead_dic[tailhead_dic[tailbn][0]][1])
        cstrt = bpy.data.objects[actob_n].pose.bones[tailbn].constraints.new("STRETCH_TO")
        cstrt.target = bpy.data.objects[actob_n]
        cstrt.subtarget = tailhead_dic[tailhead_dic[tailbn][0]][1]
