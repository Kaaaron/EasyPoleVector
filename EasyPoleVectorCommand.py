import sys
import maya.api.OpenMaya as OpenMaya
from EasyPoleVectorCore import EasyPoleVectorUI as commandUI


##########################################################
# Plug-in Command
##########################################################
class EasyPoleVectorCommand(OpenMaya.MPxCommand):
	kPluginCmdName = 'EasyPoleVectorUI'

	def __init__(self):
		OpenMaya.MPxCommand.__init__(self)

	@staticmethod
	def cmdCreator():
		return EasyPoleVectorCommand()

	def doIt(self, args):
		""" Command execution. """
		UI = commandUI.EasyPoleVectorUI()
		UI.draw()


##########################################################
# Plug-in initialization.
##########################################################

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass


def initializePlugin(mobject):
	mplugin = OpenMaya.MFnPlugin(mobject)
	try:
		mplugin.registerCommand(EasyPoleVectorCommand.kPluginCmdName, EasyPoleVectorCommand.cmdCreator)
	except:
		sys.stderr.write('Failed to register command: ' + EasyPoleVectorCommand.kPluginCmdName)


def uninitializePlugin(mobject):
	mplugin = OpenMaya.MFnPlugin(mobject)
	try:
		mplugin.deregisterCommand(EasyPoleVectorCommand.kPluginCmdName)
	except:
		sys.stderr.write('Failed to unregister command: ' + EasyPoleVectorCommand.kPluginCmdName)
