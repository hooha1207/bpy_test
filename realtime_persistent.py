import bpy
import bmesh
from bpy.app.handlers import persistent



@persistent
def update_realtime(scene=None):
    print(bpy.context.active_object.name)
    return 0.0


bpy.app.timers.register(cloth_main, persistent=True)
