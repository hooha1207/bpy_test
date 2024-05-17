import bpy
import numpy as np


m_transforms = np.array(bpy.context.active_object.matrix_world)
rt, s = np.linalg.qr(m_transforms)
s = (s[0][0], s[1][1], s[2][2])
r = rt[:3][:3]
t = m_transforms[0][3], m_transforms[1][3], m_transforms[2][3]


print('')
print('matrix\n',m_transforms)
print('scale\n',s)
print('rotation\n',r)
print('translate\n',t)
print('')
