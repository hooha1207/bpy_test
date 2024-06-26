import maya.cmds as cmds
from maya.api.OpenMaya import MVector, MMatrix, MPoint
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import math
import json
import os


file = 'weight_test.txt'
path = 'C:'+os.environ['HOMEPATH']+'/Desktop'
filepath = path+'/'+file



f = open(filepath, 'r')

for info in json.loads(f.readline()):
	dict = json.loads(info)
	obn_l = cmds.ls(u''+list(dict.keys())[0],l=True)[0]
	
	obn = cmds.ls(u''+list(dict.keys())[0])[0]
	skin_n = cmds.listConnections(obn_l+'|'+obn+'Shape', c=False, t='skinCluster')[0]
	
	for vinfo in dict[obn]:
		vid = vinfo['vid']
		bns = [i for i in vinfo.keys() if i != 'vid']
		ws = {}
		for bn in bns:
			ws[bn] = vinfo[bn]
		
		transformvalue = [] #weights
		for bn in bns:
			transformvalue.append((bn, ws[bn]))
		
		try:
			cmds.skinPercent(skin_n, obn+'.vtx['+str(vid)+']', transformValue=transformvalue, nrm=False)
		except:
			print(obn)
			print(skin_n)
f.close()
