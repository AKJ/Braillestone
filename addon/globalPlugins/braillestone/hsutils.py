import json
import os
from typing import List, Union
import api
from textInfos import POSITION_SELECTION

class cardLookup:
	def __init__(self, file):
		self.file = file

	def loadCards(self) -> list:
		file = os.path.dirname(__file__) + "\\" + self.file
		with open(file, "r", encoding="utf8") as fh:
			self.db = json.load(fh)

	def cardSearch(self, identifier: Union[int, str], param: str, multiple: bool=False) -> list:
		if multiple:
			cardlist = [item for item in self.db if item[param] == identifier]
		else:
			cardlist = next((item for item in self.db if item[param] == identifier), None)
		return cardlist


	def processCard(self, card: dict) -> dict:
		# Convert any lists into strings
		card = {key: ", ".join(value) if isinstance(value, list) else value for key, value in card.items()}
		# Clean up some strings for display
		if card["cost"]:
			card["cost"] = f"{card['cost']} mana"
		if card["type"] == "WEAPON":
			card["stats"] = f"{card['attack']} attack, {card['durability']} durability."
		elif card["type"] == "LOCATION":
			card["stats"] = f"{card['durability']} durability."
		elif card["type"] == "MINION":
			card["stats"] = f"{card['attack']} attack, {card['health']} health."
		else:
			card["stats"] = None
		keyOrder = ['name', 'cost', 'stats', 'text', 'type', 'spellSchool', 'races', 'cardClass', 'rarity', 'set', 'flavor', 'mechanics', 'artist']
		return {k: card[k] for k in keyOrder if k in card and k is not None}

	def displayCard(self, cardData: dict) -> str:
		card = self.processCard(cardData)
		if not card:
			return None
		cardstring = str()
		for k, v in card.items():
			cardstring += f"<p>{k}: {v}</p>\n"
		return cardstring

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
