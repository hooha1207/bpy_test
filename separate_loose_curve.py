#분리하고자 하는 loose curve 오브젝트를 선택하고 해당 스크립트를 실행.
#이때 separate 된 오브젝트 컨트롤은 전혀 고려하지 않았으므로, 스크립트를 실행하기 전 curve를 정리할 공간을 만들것


import bpy


actob_n = bpy.context.active_object.name



bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.curve.select_all(action='DESELECT')

for spline_id in range(len(bpy.data.objects[actob_n].data.splines)):
    if bpy.data.objects[actob_n].data.splines[0].type == "BEZIER":
        bpy.data.objects[actob_n].data.splines[0].bezier_points[0].select_control_point = True
        bpy.ops.curve.select_linked()
        bpy.ops.curve.separate()
    else:
        bpy.data.objects[actob_n].data.splines[0].points[0].select_control_point = True
        bpy.ops.curve.select_linked()
        bpy.ops.curve.separate()
    
    bpy.ops.curve.select_all(action='DESELECT')

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects[actob_n].select_set(True)
bpy.ops.object.delete(use_global=False, confirm=False)
