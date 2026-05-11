import bpy
import os
import glob

# 1. 입력 및 출력 경로 설정 (Raw String 사용)
input_dir = r"C:\Users\hooha\Desktop\clip studio Blending\motion\fbx"
output_dir = r"C:\Users\hooha\Desktop\clip studio Blending\motion\bvh"

# 2. 출력 폴더가 없다면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 3. 입력 폴더 내의 모든 fbx 파일 목록 가져오기
fbx_files = glob.glob(os.path.join(input_dir, "*.fbx"))

if not fbx_files:
    print("지정된 경로에서 FBX 파일을 찾을 수 없습니다.")

for fbx_file in fbx_files:
    # 4. 씬 초기화 및 찌꺼기 데이터(Orphan Data) 완전 삭제
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # 메모리에 남은 찌꺼기 데이터(메쉬, 아마추어, 액션 등) 재귀적 삭제
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    for action in bpy.data.actions:
        action.use_fake_user = False
    
    # 5. FBX 파일 임포트 (예외 처리 추가)
    print(f"Importing: {fbx_file}")
    try:
        bpy.ops.import_scene.fbx(filepath=fbx_file)
    except Exception as e:
        print(f"에러 발생: {fbx_file} 임포트 중 문제가 발생하여 건너뜁니다. ({e})\n")
        continue
    
    # 6. 임포트된 오브젝트 중 Armature(뼈대) 찾기
    armature = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE':
            armature = obj
            break
            
    if armature:
        # 모든 오브젝트 선택 해제 후 Armature만 활성화
        bpy.ops.object.select_all(action='DESELECT')
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        
        # 7. FBX 애니메이션 길이에 맞춰 씬의 프레임 범위 자동 조절
        if armature.animation_data and armature.animation_data.action:
            action = armature.animation_data.action
            # action.frame_range는 (시작 프레임, 끝 프레임) 튜플을 반환합니다.
            bpy.context.scene.frame_start = int(action.frame_range[0])
            bpy.context.scene.frame_end = int(action.frame_range[1])
            print(f"Frame Range 설정됨: {bpy.context.scene.frame_start} ~ {bpy.context.scene.frame_end}")
        else:
            print("경고: 애니메이션 데이터(Action)를 찾을 수 없습니다. 기본 프레임으로 진행합니다.")

        # 8. 출력될 BVH 파일 이름 생성
        base_name = os.path.basename(fbx_file)
        name_without_ext = os.path.splitext(base_name)[0]
        bvh_file = os.path.join(output_dir, name_without_ext + ".bvh")
        
        # 9. BVH 익스포트
        try:
            bpy.ops.export_anim.bvh(filepath=bvh_file)
            print(f"Exported: {bvh_file}\n")
        except Exception as e:
            print(f"에러 발생: {bvh_file} 익스포트 실패. ({e})\n")
    else:
        print(f"경고: {fbx_file} 파일에서 Armature를 찾을 수 없어 건너뜁니다.\n")

print("모든 변환 작업이 완료되었습니다!")
