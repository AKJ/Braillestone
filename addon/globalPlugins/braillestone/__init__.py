from __future__ import annotations

import gui
from globalPluginHandler import GlobalPlugin as _GlobalPlugin
from scriptHandler import script
import ui
import wx

from . import helpers
from . import hsutils

cardDb = hsutils.CardLibrary("cards.collectible.json")  # hacky placeholder
cardDb.loadCards()


class GlobalPlugin(_GlobalPlugin):
	def __init__(self) -> None:
		super().__init__()
		self.dialog = None

	@script(
		description="Look up Hearthstone card from clipboard",
		category="Braillestone",
		gesture="kb:NVDA+h"
	)
	def script_FindCardFromClipboard(self, gesture):
		selection = helpers.getSelectedText().strip()
		if selection:
			lookupCard(selection)
		else:
			ui.message("Nothing selected.")

	@script(
		description="Find Hearthstone card dialog",
		category="Braillestone",
		gesture="kb:NVDA+shift+h"
	)
	def script_FindCardDialog(self, gesture):
		if self.dialog:
			if self.dialog.IsActive():
				ui.message("dialog already open.")
				return
			else:
				self.dialog.Close()
		self.dialog = wx.TextEntryDialog(
			gui.mainFrame,
			"Enter card name to look up.",
			"Look up Hearthstone card",
			style=wx.OK | wx.CANCEL
		)
		
		def callback(result):
			if not self.dialog:
				return
			if result == wx.ID_OK:
				text = self.dialog.GetValue().strip()
				if text:
					lookupCard(text)
			self.dialog = None
		gui.runScriptModalDialog(self.dialog, callback)


def lookupCard(card: str):
	cardstring = cardDb.formatCard(card)
	res = cardDb.findCard(cardstring, "name")
	if not res:
		ui.browseableMessage(
			# Translators: The specified card could not be found
			f"Could not find card {card}.", "Card not found", isHtml=True)
		return None
	result = cardDb.displayCard(res)
	ui.browseableMessage(result, "Hearthstone Card Lookup", isHtml=True)
