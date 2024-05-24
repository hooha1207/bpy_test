import bpy
import bmesh
from bpy.app.handlers import persistent
import numpy as np 


@persistent
def update_realtime(scene=None):
    actob = bpy.context.active_object
    dg = bpy.context.evaluated_depsgraph_get()
    
    vco = np.zeros(len(actob.data.vertices)*3)
    one_step = np.ones(len(actob.data.vertices)*3)
    one_step /= 10
    actob.data.vertices.foreach_get('co', vco)
    print(vco)
    vco += one_step
    actob.data.vertices.foreach_set('co', vco)
    
    dg.update()
    return 0.0


bpy.app.timers.register(update_realtime, persistent=True)
