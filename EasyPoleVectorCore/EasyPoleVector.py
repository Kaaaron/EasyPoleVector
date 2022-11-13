import maya.cmds as cmds
import maya.api.OpenMaya as om2

"""
Original  implementation by Artem Efimovich aka Braveel:
https://github.com/Braveel
https://twitter.com/Braveel_art
"""

def get_right_place_poleVector(start: str, mid: str, end: str, isOriented: bool = False):
	jnt_01_pos = om2.MPoint(cmds.xform(start, q=1, ws=1, t=1))
	jnt_02_pos = om2.MPoint(cmds.xform(mid, q=1, ws=1, t=1))
	jnt_03_pos = om2.MPoint(cmds.xform(end, q=1, ws=1, t=1))

	vec_01 = jnt_03_pos - jnt_01_pos
	vec_02 = jnt_02_pos - jnt_01_pos

	vec_01_norm = vec_01.normal()
	proj = vec_02 * vec_01_norm
	proj_vec = vec_01_norm * proj

	vec = (vec_02 - proj_vec)
	pnt = jnt_02_pos + vec

	x = om2.MVector.kXaxisVector
	y = om2.MVector.kYaxisVector
	z = om2.MVector.kZaxisVector

	if isOriented:
		y = (vec_01 ^ vec_02).normal()
		x = vec_01_norm
		z = (-vec).normal()

	return [x[0], x[1], x[2], 0,
			y[0], y[1], y[2], 0,
			z[0], z[1], z[2], 0,
			pnt[0], pnt[1], pnt[2], 1]


def create_right_place_poleVector(start: str, mid: str, end: str, handle: str, isOriented: bool = False):
	pole = cmds.spaceLocator()
	matrix = get_right_place_poleVector(start, mid, end, isOriented)
	cmds.xform(pole, ws=1, m=matrix)

	cmds.poleVectorConstraint(pole, handle)
