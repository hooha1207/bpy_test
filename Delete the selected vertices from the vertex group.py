import bpy


bpy.ops.object.mode_set(mode='OBJECT')

selOb = bpy.context.selected_objects


for ob in selOb:
    vertList_idx = [vertex.index for vertex in ob.data.vertices if vertex.select]
    bpy.context.view_layer.objects.active = ob
    
    for vertex_group in bpy.context.object.vertex_groups:
        vertex_group.remove(vertList_idx)
        
# how to use
# 오브젝트의 edit mode로 진입한 뒤 모든 vertex group에서 weight를 삭제하고자 하는 vertex 선택
# 해당 코드 실행

# 혹은 edit mode에서 모든 vertex group에서 값을 삭제할 vertex를 선택한 뒤 
# F3을 눌러 remove from all 을 검색해서 실행하기
# 이럼 위 코드를 실행한 것과 같은 결과를 얻음
