import bpy


actOb = bpy.context.object
selOb = bpy.context.selected_objects[1]
selOb = [i for i in bpy.context.selected_objects if not i == actOb]
selOb = selOb[0]

selOb_bones = selOb.pose.bones.keys()

bpy.ops.object.mode_set(mode='POSE')


for bone in actOb.pose.bones:
    
    if not bone.name in selOb_bones:
        continue
    
    cstrt = bone.constraints.new("COPY_LOCATION")
    cstrt.target = selOb
    cstrt.subtarget = bone.name
    cstrt.target_space = "LOCAL"
    cstrt.owner_space = "LOCAL"


bpy.ops.object.mode_set(mode='OBJECT')



#해당 스크립트는 amarture를 duplicate 해서 controller를 만들 때 copy location을 일괄 적용해주는 스크립트다
#cloth wrinkle bone을 figure bone에서 분리하여 컨트롤하기 위해 만들었다
