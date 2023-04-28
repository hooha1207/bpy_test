import bgl
import bpy
import gpu
import numpy as np


# Find render result
render_result = bpy.data.images['blender_community_badge_orange.png']

# Create a GPU texture that shares GPU memory with Blender
gpu_tex = gpu.texture.from_image(render_result)

# Read image from GPU
#gpu_tex.read()

# OR read image into a NumPy array (might be more convenient for later operations)
fbo = gpu.types.GPUFrameBuffer(color_slots=(gpu_tex,))

buffer_np = np.empty(gpu_tex.width * gpu_tex.height * 4, dtype=np.float32)
buffer = bgl.Buffer(bgl.GL_FLOAT, buffer_np.shape, buffer_np)
with fbo.bind():
    bgl.glReadBuffer(bgl.GL_BACK)
    bgl.glReadPixels(0, 0, gpu_tex.width, gpu_tex.height, bgl.GL_RGBA, bgl.GL_FLOAT, buffer)

# Now the NumPy array has the pixel data, you can reshape it and/or export it as bytes if you wish
print(buffer_np)
# 이미지가 1차원의 시퀀스로 변환되어서 buffer_np에 저장되므로 .shape 메소드를 이용해서 reshape을 할 필요가 있다
# 출처 : https://blender.stackexchange.com/questions/2170/how-to-access-render-result-pixels-from-python-script
