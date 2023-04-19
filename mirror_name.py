import bpy


new_bone_name = 'eyeline_inner'



for bone in bpy.context.selected_pose_bones:
    if bone.head[0] < 0:
        #type left
        bone.name = f'{new_bone_name}'
        bone.name = f'{bone.name}.L'


for bone in bpy.context.selected_pose_bones:
    if bone.head[0] > 0:
        #type right
        bone.name = f'{new_bone_name}'
        bone.name = f'{bone.name}.R'


#shape to bone 혹은 curve to bone으로 새로 생성한 bone의 경우,
#이름이 좌우 구분을 할 수 없게 되어있어 이를 극복하고자 작성.
#curve to bone 혹은 shape to bone으로 생성해서 bone이 좌우 구분이 안되는 bone을 선택하고 해당 코드를 실행하면,
#x축 기준 bone 이름을 좌우구분하여 적용해서 mirror 적용 가능
