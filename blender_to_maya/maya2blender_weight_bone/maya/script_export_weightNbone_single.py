import maya.cmds as cmds
from maya.api.OpenMaya import MVector, MMatrix, MPoint
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import re
import math
import json


"""
export 하고자 하는 mesh와 해당 mesh와 연결된 skin cluster를 선택한다
path 변수에 입력된 경로가 존재하는지 확인 및
해당 경로가 내가 blender에서 불러올 경로가 맞는지 확인한다
스크립트를 실행한다
"""



SKINCLUSTER = cmds.ls(sl=True,l=True, et='skinCluster')[0]
SHAPENAME = [i for i in cmds.ls(sl=True,l=True) if i!=SKINCLUSTER][0]

file_weight = 'weight_test_' + SHAPENAME.split('|')[-1] + '.json'
path = 'C:'+os.environ['HOMEPATH']+'/Desktop/tmp/test'
filepath_weight = path+'/'+file_weight

file_bone = 'bone_test_'+ SHAPENAME.split('|')[-1] +'.json'
filepath_bone = path+'/'+file_bone


f = open(filepath_weight, 'w+')
f.close()
f = open(filepath_bone, 'w+')
f.close()

#SKINCLUSTER = cmds.ls(sl=True,l=True, et='skinCluster')[0]
#SHAPENAME = [i for i in cmds.ls(sl=True,l=True) if i!=SKINCLUSTER][0]

#print(SKINCLUSTER)
#print(SHAPENAME)


mesh_path = om.MSelectionList().add(SHAPENAME).getDagPath(0)
skin_cluster = oma.MFnSkinCluster(om.MSelectionList().add(SKINCLUSTER).getDependNode(0))

inf_dags = skin_cluster.influenceObjects()
#print([i.fullPathName() for i in inf_dags])
inf_index = om.MIntArray()
for x in range(len(inf_dags)):
	inf_index.append(int(skin_cluster.indexForInfluenceObject(inf_dags[x])))

component = om.MFnSingleIndexedComponent()
vertex_comp = component.create(om.MFn.kMeshVertComponent)

indices = [int(re.findall(r'\d+', vert)[-1]) for vert in cmds.ls(SHAPENAME+'.vtx[*]', fl=1)]
component.addElements(indices)

path, comp, infs, dags, sk = [mesh_path, vertex_comp, inf_index, inf_dags, skin_cluster]
#weights = sk.getWeights(path, comp, infs)
weights = sk.getWeights(mesh_path, vertex_comp, inf_index)



total_json = []
inf_name = [i.fullPathName() for i in inf_dags]

for i in range(len(weights) // len(inf_index)):
	dict = {'vid':i}
	
	for inf_i in range(len(inf_index)):
		dict[inf_name[inf_i]] = weights[i*len(inf_index) + inf_i]
	
	total_json.append(dict)


f = open(filepath_weight, 'a')
f.write(json.dumps(total_json))
f.close()

def get_world_transform (obj):
	return om.MTransformationMatrix( MMatrix ( cmds.xform( obj, q=True, matrix=True, ws=True ) ))


binfo = []
for bn in inf_name:
	dict = {'bn':bn}
	
	matrix = get_world_transform(bn)
	
	loc_x, loc_y, loc_z = matrix.translation(1)
	sc_x, sc_y, sc_z = matrix.scale(1)
	rot_x, rot_y, rot_z = matrix.rotation(1).asEulerRotation()

	dict['loc_x'] = loc_x
	dict['loc_y'] = loc_y
	dict['loc_z'] = loc_z
	
	dict['sc_x'] = sc_x
	dict['sc_y'] = sc_y
	dict['sc_z'] = sc_z
	
	dict['rot_x'] = rot_x
	dict['rot_y'] = rot_y
	dict['rot_z'] = rot_z
	
	binfo.append(dict)

f = open(filepath_bone, 'a')
f.write(json.dumps(binfo))
f.close()
