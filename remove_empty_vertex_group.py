#선택한 mesh object가 가지고 있는 vertex group 중 값이 아무것도 없는
#즉 empty vertex group 을 삭제하는 코드다
#오브젝트를 선택하고 코드를 실행하면 삭제된다
#reference: https://blender.community/c/rightclickselect/PQpn/?sorting=hot


import bpy


def make_group_list():
    obj = []
    temp_list = []
    group_list = []
    so = bpy.context.selected_objects
    for i in so:
        obj.append(i)
        for i in obj:
            #I've used .extend here (with square brackets) to add every item to the list
            temp_list.extend([group[0] for group in i.vertex_groups.items()])
            for group_name in temp_list:
                if group_name not in group_list:
                    group_list.append(group_name)
    return group_list


#2. CHECK THE AVERAGE WEIGHT OF EACH VERTEX POINT
def average_weight(vertex_group_names, obj):
    mesh = obj.data
    for vertex in mesh.vertices:
        for group in vertex.groups:
            if group.group in vertex_group_names and group.weight > 0.1:
                return False
    return True


#3. DELETE THE GROUP
def delete_group(obj, vertex_group):
    obj.vertex_groups.remove(vertex_group)

# GROUP_LIST DEFINED
group_list = make_group_list()

#4. MAIN FOR LOOP
for obj in bpy.context.selected_objects: 
    for vertex_group_name in group_list:
        vertex_group = obj.vertex_groups.get(vertex_group_name)
        if vertex_group is not None:
            if average_weight([vertex_group.index], obj):
                delete_group(obj,vertex_group)
