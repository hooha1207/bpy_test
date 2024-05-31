import bpy


#meshdeform 이름을 deform으로 바꿔야 됨


for ob in bpy.context.selected_objects:
    bpy.ops.object.meshdeform_bind({'object':ob, 'active_object':ob, 'scene':bpy.data.scenes['Scene']}, modifier="deform")