#weight 값을 얻고자 하는 object의 데이터와 해당 object가 가지고 있는 vertex group 중 값을 취하고 싶은 vertex group을 넣어준다
#결과 값은 generator 이므로, list로 형변환시켜서 사용하면 된다
#결과 값은 vertex index마다 부여된 vertex weight 값이 tuple로 묶인 list가 로 반환된다
#reference = https://blender.stackexchange.com/questions/46834/how-can-i-get-the-weight-for-all-vertices-in-a-vertex-group

import bpy

def get_weights(ob, vgroup):
    group_index = vgroup.index
    for i, v in enumerate(ob.data.vertices):
        for g in v.groups:
            if g.group == group_index:
                yield (i, g.weight)
                break
            

print(list(get_weights(bpy.data.objects['Cube'], bpy.data.objects['Cube'].vertex_groups[0])))
