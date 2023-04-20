import bpy
import math



import bpy
for obj in bpy.context.selected_objects:
    for modif in obj.modifiers:
        obj.modifiers.remove(modif)
#선택한 오브젝트의 modifier를 전부 삭제한다
#해당 기능은 blender ui로 사용할 수 없어 기록한다


bpy.ops.object.mode_set(mode='POSE')
bpy.ops.pose.copy()
bpy.ops.pose.paste(flipped=True)
#pose를 flip 즉 반전시켜서 붙여넣는다
#mirror 혹은 symmetric이랑은 다르다


bpy.data.objects['Armature'].data.bones.active
#Armature 란 이름을 가진 오브젝트(armature)에서 active select 된 bone을 출력한다


bpy.data.objects['Armature'].pose.bones['Bone'].bone.select
#Armature 란 이름을 가진 오브젝트(armature)가 pose mode일 때 bone을 select 상태를 bool로 출력한다
bpy.data.objects['Armature'].pose.bones['Bone'].bone.select = True
#Armature 란 이름을 가진 오브젝트(armature)가 pose mode일 때 Bone이란 이름을 가진 bone을 select 상태를 True로 만들어준다
bpy.data.objects['Armature'].pose.bones['Bone'].bone.select = False
#Armature 란 이름을 가진 오브젝트(armature)가 pose mode일 때  Bone이란 이름을 가진 bone을 select 상태를 False로 만들어준다

bpy.data.objects['Armature'].data.edit_bones['Bone'].bone.select
#Armature 란 이름을 가진 오브젝트(armature)가 EDIT mode일 때 bone을 select 상태를 bool로 출력한다
bpy.data.objects['Armature'].data.edit_bones['Bone'].bone.select = True
#Armature 란 이름을 가진 오브젝트(armature)가 EDIT mode일 때 bone을 select 상태를 True로 만들어준다
bpy.data.objects['Armature'].data.edit_bones['Bone'].bone.select = False
#Armature 란 이름을 가진 오브젝트(armature)가 EDIT mode일 때 bone을 select 상태를 False로 만들어준다



choose_layer_index = 0
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    bpy.context.object.data.layers[bone_layer_index] = True
for bone_layer_index in range(len(bpy.context.object.data.layers)):
    if bone_layer_index == choose_layer_index:
        continue
    bpy.context.object.data.layers[bone_layer_index] = False
#bone layer의 경우, 무조건 하나 이상 활성화되어야만 된다
#때문에 원하는 bone layer를 선택하려면, 전체를 활성화한 다음,
#원하는 bone layer 외에는 전부 비활성화하는 과정이 필요하다
#위 코드는 해당 과정을 수행한다



bpy.ops.object.mode_set(mode='POSE')
for bone_layer in range(len(bpy.context.object.data.layers)):
  bpy.context.object.data.layers[bone_layer] = True
#armature 객체를 선택한 뒤, pose모드에 진입한다
#pose모드에 진입한 뒤 bone_layer를 슬라이싱으로 접근하여 모든 layer를 활성화한다


bpy.ops.mesh.select_mirror()


actOb = bpy.context.object
org_co = bpy.context.object.matrix_world.to_translation()
actOb_sc = bpy.context.object.matrix_world.to_scale()
vertList = [((actOb_sc*vertex.co) + org_co) for vertex in actOb.data.vertices if vertex.select]
#선택된 오브젝트의 선택된 mesh vetex 좌표를 world space로 얻을 수 있다
#mesh vertex 좌표는 mesh vertex 좌표에 origin 좌표를 더해서 구할 수 있다
#이때 오브젝트의 scale을 mesh vertex 좌표에 곱해주면 scale을 apply한 좌표 값을 얻을 수 있다
actOb = bpy.context.object
org_co = bpy.context.object.matrix_world.to_translation()
vertList = [(org_co + vertex.co) for vertex in actOb.data.vertices if vertex.select]
#선택된 오브젝트의 선택된 mesh vetex 좌표를 world space로 얻을 수 있다
#mesh vertex 좌표는 mesh vertex 좌표에 origin 좌표를 더해서 구할 수 있다
actOb = bpy.context.object
vertList = [(vertex.co) for vertex in actOb.data.vertices if vertex.select]
#선택된 오브젝트의 선택된 mesh vetex 좌표를 local space로 얻을 수 있다
bpy.context.object.matrix_world.to_translation()
#오브젝트의 origin을 출력할 수 있다

bpy.context.scene.frame_current
#현재 키프레임 지점을 출력할 수 있다
bpy.context.scene.frame_start
#키프레임 시작 지점을 출력할 수 있다
bpy.context.scene.frame_end
#키프레임 끝 지점을 출력할 수 있다

bpy.context.scene.frame_set(1)
#키프레임을 1로 이동시킬 수 있다

bpy.ops.screen.animation_play()
#애니메이션 play

bpy.ops.screen.animation_cancel()
#애니메이션을 실행하기 전으로 돌아간다
#ui로 비유하자면, 애니메이션 실행 중 esc키를 누른 것과 같다

bpy.ops.screen.keyframe_jump()
#다음 키프레임으로 timeline을 옮겨주는 기능이다
#단축키로 말하자면, 키보드 up arrow 키와 동일한 동작을 한다
bpy.ops.screen.keyframe_jump(next=False)
#이전 키프레임으로 timeline을 옮겨주는 기능이다
#단축키로 말하자면, 키보드 down arrow 키와 동일한 동작을 한다

bpy.context.scene.objects.get("Cube")
#이름이 Cube인 오브젝트 정보를 가져온다

bpy.context.view_layer.objects.active = bpy.context.scene.objects.get("Cube")
#활성 오브젝트를 Cube 오브젝트로 바꿔주는 기능이다
#해석해보자면, 오브젝트 이름이 Cube라 정의되어있는 오브젝트로 활성 오브젝트를 바꿔준다는 뜻이다
#이때 active 오브젝트를 바꾼다고 select가 바뀌는 건 아니므로 주의하자

bpy.ops.object.select_all(action='DESELECT')
#select 오브젝트가 전부 deselect 된다

bpy.data.objects['Cube'].select_set(True)
bpy.data.objects['Cube.001'].select_set(True)
#이름이 Cube인 오브젝트를 active select로 선택하게 된다
#이때 이름을 Cube.001로 바꿔서 다시 실행하면, active select이 Cube.001로 바뀌고 이전에 선택했던 오브젝트는 select로 바뀌게 된다
#ui로 비유하자면, 마우스 왼쪽 클릭과 똑같은 동작을 한다

bpy.context.selected_objects
#선택된 오브젝트 정보를 리스트로 묶어 가져온다
bpy.context.selected_objects[0]
#선택된 오브젝트의 outliner 정렬 0번째 오브젝트를 가져온다

bpy.context.selected_objects[0].location
#선택된 오브젝트의 outliner 정렬 0번째 오브젝트의 location 정보를 가져온다
bpy.context.selected_objects[0].rotation_euler
bpy.context.selected_objects[0].rotation_quaternion
#선택된 오브젝트의 outliner 정렬 0번째 오브젝트의 rotation 정보를 가져온다
#둘의 차이는 rotation 축 설정이 뭐로 정의되어있냐에 따라 다르게 사용해야 된다

bpy.context.selected_objects[0].modifiers.items()
bpy.context.selected_objects[0].modifiers.values()
bpy.context.selected_objects[0].modifiers.keys()
#선택된 오브젝트의 outliner 정렬 0번째 오브젝트의 부여된 modifier 정보를 모두 가져온다
#셋의 차이점은 추출하는 정보의 데이터 타입이 다르므로 알맞게 사용하자
#items는 modifier 이름과 modifier 객체 정보를 리스트로 묶어서 반환하지만,
#values는 modifier 객체 정보만 반환한다
#keys는 modifier 이름만 반환한다

bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
#오브젝트를 복사하고 그대로 붙여넣는다
#단축키로 비유하자면, shift + d 와 같다

bpy.ops.object.select_by_type(type='MESH')
#type이 mesh인 오브젝트를 전부 선택해주는 기능이다
bpy.ops.object.select_by_type(type='ARMATURE')
#type이 armature인 오브젝트를 전부 선택해주는 기능이다
bpy.ops.object.select_by_type(type='LIGHT')
#type이 light인 오브젝트를 전부 선택해주는 기능이다
bpy.ops.object.select_by_type(type='CAMERA')
#type이 camera인 오브젝트를 전부 선택해주는 기능이다

bpy.context.active_object.animation_data
#keyframe 애니메이션 데이터가 있으면, 어떤 애니메이션이 존재하는지 반환한다
#만약 없으면, None을 반환한다

bpy.context.object
#active select 된 객체의 bpy.data.objects['이름'] 정보를 가져온다

bpy.context.object.dimensions
#active select 된 객체의 dimension 정보를 Vector((1,1,1)) 형태로 가져온다
bpy.context.object.dimensions.x
#active select 된 객체의 dimension x 정보를 float 형태로 가져온다
#x 대신 y, z도 가능하다
bpy.context.object.dimensions[0]
#active select 된 객체의 dimension x 정보를 float 형태로 가져온다
#0 대신 1, 2도 가능하다

bpy.context.object.location
#active select 된 객체의 location 정보를 Vector((0,0,0)) 형태로 가져온다
bpy.context.object.location.x
#active select 된 객체의 location x 정보를 float 형태로 가져온다
#x 대신 y, z도 가능하다

bpy.context.object.rotation_euler
#active select 된 객체의 rotation_euler 정보를 math.radians로 변환한 Euler((1.5,0,1.5), 'XYZ') 형태로 가져온다
bpy.context.object.rotation_mode = 'XZY'
#rotation_euler 축을 XZY 순으로 바꿔준다
bpy.context.object.rotation_euler[0] = math.radians(각도)
#rotation_euler 정보 중 x를 각도 값으로 바꿔준다

bpy.ops.object.modifier_add(type='BOOLEAN')
#이름으로 지정한 객체에 booean modifier를 적용시킨다
bpy.data.objects['이름'].modifiers['Boolean'].object = bpy.data.objects['이름2']
#boolean 연산에 사용될 보조 객체를 지정한다
bpy.data.objects['이름'].modifiers['Boolean'].operation = 'INTERSECT'
#boolean 연산을 intersect로 바꿔준다
#UNION, DIFFERENCE도 가능하다

bpy.context.scene.objects['이름'].keyframe_insert(data_path='location', frame=1)
#이름으로 지정한 객체의 location 값을 키프레임 1에 저장한다



## blender module install 하는 방법
"""
아래 영상은 Blender Foundation\Blender 3.0\3.0\python\lib\site-packages 폴더 안에 module을 넣어주는 방법에 대해 서술한 영상이다  
https://youtu.be/DSU1Q-utQ_w  

한 번 설치하면, 내가 삭제하지 않는 한 영구적으로 쓸 수 있다  
"""


import pip
pip.main(['install', 'torch'])
#위 코드는 만약 blender에 pip이 존재할 경우 손쉽게 pytorch를 설치하는 코드다
#cmd에서 pip install 하는 것과 같다
pip.main(['install', 'torchvision'])
#위 코드는 만약 blender에 pip이 존재할 경우 손쉽게 pytorch를 설치하는 코드다
#cmd에서 pip install 하는 것과 같다
