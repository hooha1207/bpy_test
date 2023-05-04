#reference = https://blender.stackexchange.com/questions/42778/how-to-merge-vertex-groups

#이름이 vertex_A_name으로 정의된 vertex group에 vertex_B_name의 값을 더해준다


import bpy


vgroup_A_name = "Group"
vgroup_B_name = "Group.001"

# Get both groups and add them into third
ob = bpy.context.active_object

#vgroup = ob.vertex_groups.new(name=vgroup_A_name+"+"+vgroup_B_name)
vgroup = ob.vertex_groups[vgroup_A_name]

for id, vert in enumerate(ob.data.vertices):
    available_groups = [v_group_elem.group for v_group_elem in vert.groups]
    A = B = 0
    if ob.vertex_groups[vgroup_A_name].index in available_groups:
        A = ob.vertex_groups[vgroup_A_name].weight(id)
    if ob.vertex_groups[vgroup_B_name].index in available_groups:
        B = ob.vertex_groups[vgroup_B_name].weight(id)

    # only add to vertex group is weight is > 0
    sum = A + B
    vgroup.add([id], sum ,'ADD')
