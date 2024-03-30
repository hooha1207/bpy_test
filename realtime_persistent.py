import bpy
import bmesh
from bpy.app.handlers import persistent



@persistent
def cloth_main(scene=None):
    print(bpy.context.active_object.name)
    return 0.0


bpy.app.timers.register(cloth_main, persistent=True)