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

### 해당 계산은 추후 다른 툴에서 matrix to s,r,t가 안될 때를 대비해서 작성했다.
### 기본적으로 matrix to s,r,t는 지원한다면 해당 기능을 사용할 것
