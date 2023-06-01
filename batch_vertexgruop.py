# vertex weight를 잘못 적용했는데, 이를 일괄 수정하는 스크립트

import bpy


bpy.ops.object.mode_set(mode='OBJECT')

selOb = bpy.context.selected_objects


for ob in selOb:
    vertList = [vertex for vertex in ob.data.vertices]
#    bpy.context.view_layer.objects.active = ob
    
    group_id = []
    for vertex_group in bpy.context.object.vertex_groups:
        if 'Bone' in vertex_group.name:
            group_id.append(vertex_group.index)
    
    for v in vertList:
        for vg in v.groups:
            if vg.group in group_id:
                vg.weight = 1
        
# how to use
# 오브젝트의 edit mode로 진입한 뒤 모든 vertex group에서 weight를 삭제하고자 하는 vertex 선택
# 해당 코드 실행

# 혹은 edit mode에서 모든 vertex group에서 값을 삭제할 vertex를 선택한 뒤 
# F3을 눌러 remove from all 을 검색해서 실행하기
# 이럼 위 코드를 실행한 것과 같은 결과를 얻음

# 굳이 이렇게 코드로 기록을 남기는 이유는,
# 특정 vertex group에서는 값을 삭제하지 않게 하기 
