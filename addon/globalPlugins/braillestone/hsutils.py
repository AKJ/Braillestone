import json
import os
from typing import List, Union

class CardLookup:
	def __init__(self, file):
		self.file = file

	def loadCards(self) -> list:
		file = os.path.dirname(__file__) + "\\" + self.file
		with open(file, "r", encoding="utf8") as fh:
			self.db = json.load(fh)

	def findCard(self, identifier: Union[int, str], param: str, multiple: bool=False) -> list:
		if multiple:
			cardlist = [item for item in self.db if item[param] == identifier]
		else:
			cardlist = next((item for item in self.db if item[param] == identifier), None)
		return cardlist

	def formatCard(self, cardstring: str) -> str:
		if "’" in cardstring:
			cardstring = cardstring.replace("’", "'")
		LITTLE_WORDS = ['a', 'an', 'and', 'for', 'in', 'of', 'on', 'the', 'to']
		card = " ".join(w.capitalize() if w not in LITTLE_WORDS else w for w in cardstring.split())
		return card

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
