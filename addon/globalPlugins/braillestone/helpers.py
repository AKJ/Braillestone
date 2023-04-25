import os
import sys
import contextlib
import api
from textInfos import POSITION_SELECTION

PLUGIN_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
LIB_DIRECTORY = os.path.join(PLUGIN_DIRECTORY, "lib")


@contextlib.contextmanager
def import_bundled(packages_path=LIB_DIRECTORY):
	sys.path.insert(0, packages_path)
	try:
		yield
	finally:
		sys.path.remove(packages_path)


# adapted from Quick Dictionary by Oleksandr Gryshchenko <grisov.nvaccess@mailnull.com>
def getSelectedText() -> str:
	"""Retrieve the selected text.
	If the selected text is missing - extract the text from the clipboard.
	If the clipboard is empty or contains no text data - announce a warning.
	@return: selected text, text from the clipboard, or an empty string
	@rtype: str
	"""
	obj = api.getFocusObject()
	treeInterceptor = obj.treeInterceptor
	if hasattr(treeInterceptor, 'TextInfo') and not treeInterceptor.passThrough:
		obj = treeInterceptor
	try:
		info = obj.makeTextInfo(POSITION_SELECTION)
	except (RuntimeError, NotImplementedError):
		info = None
	if not info or info.isCollapsed:
		try:
			text = api.getClipData()
		except Exception:
			text = ''
		if not text or not isinstance(text, str):
			# Translators: User has pressed the shortcut key for translating selected text,
			# but no text was actually selected and clipboard is clear
			ui.message(_("There is no selected text, the clipboard is also empty, or its content is not text!"))
			return ''
		return text
	return info.text
