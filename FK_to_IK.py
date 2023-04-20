import bpy


actob = bpy.context.object


bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='POSE')


constraints_name = "FK_to_IK_COPY_TRANSFORMS"
cstrt_LOC_name = "foot_location"

for bone in bpy.context.selected_pose_bones:

    if "total" in bone.name:
        continue
    elif bone.name[-2:] in [".L",".R"]:            
        cstrt = bone.constraints.new("COPY_TRANSFORMS")
        cstrt.name = constraints_name
        cstrt.target = actob
        if "_poletarget" in bone.name:
            cstrt.subtarget = actob.pose.bones[f"{bone.name[:-15]}FK_poletarget{bone.name[-2:]}"].name
            continue
        cstrt.subtarget = actob.pose.bones[f"{bone.name[:-4]}FK{bone.name[-2:]}"].name
        if "Foot" in bone.name:
            cstrt_LOC = bone.constraints.new("COPY_LOCATION")
            cstrt_LOC.name = cstrt_LOC_name
            cstrt_LOC.target = actob
            cstrt_LOC.subtarget = f"Leg.FK{bone.name[-2:]}"
            cstrt_LOC.head_tail = 1

    else:
        cstrt = bone.constraints.new("COPY_TRANSFORMS")
        cstrt.name = constraints_name
        cstrt.target = actob
        cstrt.subtarget = actob.pose.bones[f"{bone.name[:-3]}.FK"].name
    
bpy.ops.pose.visual_transform_apply()


for bone in bpy.context.selected_pose_bones:

    if "total" in bone.name:
        continue
    elif "Foot" in bone.name:
        bone.constraints.remove(bone.constraints.get(cstrt_LOC_name))
#    bone.constraints[constraints_name].enabled = False
    bone.constraints.remove(bone.constraints.get(constraints_name))
    
bpy.ops.object.mode_set(mode='OBJECT')
