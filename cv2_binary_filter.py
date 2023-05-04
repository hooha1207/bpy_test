import cv2
import bpy


img_n = 'toon_shading_test'
threshold1 = 125
threshold2 = 250

bpy.context.scene.use_nodes = True
bpy.context.scene.view_layers["ViewLayer"].use_pass_diffuse_direct = True




bpy.context.scene.render.filepath = f"C:/blender/tmp_render_img/{img_n}"
bpy.ops.render.render(write_still=True)


shadow_img = cv2.imread(f"C:/blender/tmp_render_img/{img_n}.png")

ret, process_img = cv2.threshold(shadow_img, threshold1, threshold2, cv2.THRESH_BINARY)
cv2.imwrite(f"C:/blender/tmp_render_img/{img_n}_after.png", process_img)


bpy.ops.image.open(filepath=f"C:\\blender\\tmp_render_img\\{img_n}_after.png", directory="C:\\blender\\tmp_render_img\\", files=[{"name":f"{img_n}_after.png", "name":f"{img_n}_after.png"}], relative_path=True, show_multiview=True)
img = bpy.data.images[f"{img_n}_after.png"]

for area in bpy.context.screen.areas:
    if area.type == 'IMAGE_EDITOR':
        area.spaces.active.image = img
