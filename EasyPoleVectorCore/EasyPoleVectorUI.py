from EasyPoleVectorCore import EasyPoleVector as eapv
import maya.cmds as cmds


class EasyPoleVectorUI:
	def __init__(self):
		self.start: str = ""
		self.mid: str = ""
		self.end: str = ""
		self.handle: str = ""

		# UI fields
		self.startfield: str = ""
		self.midfield: str = ""
		self.endfield: str = ""
		self.handlefield: str = ""

		self.windowName: str = "EasyPoleVectorUI"
		self.windowWidth: int = 275
		self.windowHeight: int = 100

	def _smart_find_from_effector(self, Effector: str):

		# A bit of ugly try-except ahead.
		# This just means that there is no valid node available in the retrieved list that we can use.
		# In those cases there is not really sth that the smart-pick can do, except continue.

		try:
			self.mid = cmds.listRelatives(Effector, p=True)[0]
		except TypeError:
			print("Could not smart pick a value for 'mid'.")

		if cmds.objExists(self.mid):
			try:
				self.start = cmds.listRelatives(self.mid, p=True)[0]
			except TypeError:
				print("Could not smart pick a value for 'start'.")

			try:
				self.end = cmds.listRelatives(self.mid, c=True)[0]
			except TypeError:
				print("Could not smart pick a value for 'end'.")

		try:
			self.handle = cmds.listConnections(Effector, type='ikHandle')[0]
		except TypeError:
			print("Could not smart pick a value for 'handle'.")

		self._refresh_all_fields()

	def _smart_find_from_handle(self, ikHandle: str):
		try:
			# find effector as an incoming connection, then just find from effector
			effector: str = cmds.listConnections(ikHandle, type='ikEffector')[0]
			self._smart_find_from_effector(effector)
		except TypeError:
			print("Could not smart pick from ikHandle.")

	def _smart_find_from_start(self, StartNode: str):

		self._refresh_all_fields()

	def _smart_fill(self, *args):
		"""
		Try to auto fill all fields based on selection.
		"""
		currentSelection = cmds.ls(sl=True)
		if not currentSelection:
			return

		currentSelection = currentSelection[0]

		if cmds.objectType(currentSelection, isType='ikEffector'):
			self._smart_find_from_effector(currentSelection)
			return

		if cmds.objectType(currentSelection, isType='ikHandle'):
			self._smart_find_from_handle(currentSelection)
			return

		self._smart_find_from_start(currentSelection)

	def _create(self, *args):
		eapv.create_right_place_poleVector(
			self.start,
			self.mid,
			self.end,
			self.handle)

	def _refresh_startfield(self):
		cmds.textField(self.startfield, text=self.start, e=True)

	def _set_start_by_selection(self, *args):
		self.start = cmds.ls(dagObjects=True, sl=True)[0]
		self._refresh_startfield()

	def _set_start_by_content(self, *args):
		self.start = cmds.textField(self.startfield, text=True, q=True)

	def _refresh_midfield(self):
		cmds.textField(self.midfield, text=self.mid, e=True)

	def _set_mid_by_selection(self, *args):
		self.mid = cmds.ls(dagObjects=True, sl=True)[0]
		self._refresh_midfield()

	def _set_mid_by_content(self, *args):
		self.mid = cmds.textField(self.midfield, text=True, q=True)

	def _refresh_endfield(self):
		cmds.textField(self.endfield, text=self.end, e=True)

	def _set_end_by_selection(self, *args):
		self.end = cmds.ls(dagObjects=True, sl=True)[0]
		self._refresh_endfield()

	def _set_end_by_content(self, *args):
		self.end = cmds.textField(self.endfield, text=True, q=True)

	def _refresh_handlefield(self):
		cmds.textField(self.handlefield, text=self.handle, e=True)

	def _set_handle_by_selection(self, *args):
		selection = cmds.ls(dagObjects=True, sl=True, typ="ikHandle")
		if len(selection) > 0:
			self.handle = selection[0]
		self._refresh_handlefield()

	def _set_handle_by_content(self, *args):
		self.handle = cmds.textField(self.handlefield, text=True, q=True)

	def _refresh_all_fields(self):
		self._refresh_startfield()
		self._refresh_midfield()
		self._refresh_endfield()
		self._refresh_handlefield()

	def draw(self):
		# make sure we don't have another one open to avoid "20 hidden windows"-situations
		if cmds.window(self.windowName, exists=True):
			cmds.deleteUI(self.windowName)

		window = cmds.window(self.windowName, title="Easy Pole Vector")
		cmds.window(self.windowName, e=True, w=self.windowWidth, height=self.windowHeight, resizeToFitChildren=True)  # for some reason the width needs to be specified after creation, if a windowname is specified.

		masterLayout = cmds.columnLayout(width=self.windowWidth)
		cmds.showWindow(window)

		# =================================== data ui ===================================
		textColWidth: int = 85
		applyBtnColWidth: int = 50
		textFieldColWidth: int = self.windowWidth - textColWidth - applyBtnColWidth

		cmds.setParent(masterLayout)
		btnLayout = cmds.rowColumnLayout(
			numberOfColumns=3,
			p=masterLayout,
			width=self.windowWidth,
			columnSpacing=[(2, 5)],
			columnWidth=[(1, textColWidth),
						(2, textFieldColWidth),
						(3, applyBtnColWidth)])

		cmds.text(l="Chain start: ", align='right')
		self.startfield = cmds.textField(changeCommand=self._set_start_by_content)
		cmds.button(l="<<", c=self._set_start_by_selection, rs=False, align='left')

		cmds.setParent(btnLayout)
		cmds.text(l="Chain middle: ", align='right')
		self.midfield = cmds.textField(changeCommand=self._set_mid_by_content)
		cmds.button(l="<<", c=self._set_mid_by_selection, rs=False, align='left')

		cmds.setParent(btnLayout)
		cmds.text(l="Chain end: ", align='right')
		self.endfield = cmds.textField(changeCommand=self._set_end_by_content)
		cmds.button(l="<<", c=self._set_end_by_selection, rs=False, align='left')

		sepHeight = 5
		cmds.setParent(btnLayout)
		cmds.separator(h=sepHeight, vis=False)
		cmds.separator(h=sepHeight, vis=False)
		cmds.separator(h=sepHeight, vis=False)

		cmds.setParent(btnLayout)
		cmds.text(l="IK Handle: ", align='right')
		self.handlefield = cmds.textField(changeCommand=self._set_handle_by_content)
		cmds.button(l="<<", c=self._set_handle_by_selection, rs=False, align='left')

		cmds.setParent(masterLayout)
		cmds.separator(h=10)

		# =================================== Main Buttons ===================================

		cmds.setParent(masterLayout)
		cmds.rowColumnLayout(numberOfColumns=2, width=self.windowWidth, columnSpacing=[(2, 5)])
		cmds.button(l="Smart fill", rs=False, c=self._smart_fill, w=self.windowWidth / 2)
		cmds.button(l="Create Pole Vector", rs=False, c=self._create, w=self.windowWidth / 2)

		# initial fill
		self._smart_fill()


if __name__ == "__main__":
	UI = EasyPoleVectorUI()
	UI.draw()
