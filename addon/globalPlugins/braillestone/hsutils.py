from __future__ import annotations

import re
import requests
from logHandler import log

class HearthstoneAPI:
	"""
	A wrapper for pulling card definition files from the Hearthstone JSON API
	"""

	def __init__(
			self, base_url: str = "https://api.hearthstonejson.com/v1/", build: str = "latest/", locale: str = "enUS/"):
		self.url = f"{base_url}{build}{locale}"

	def get(self, endpoint: str = "cards.json"):
		fullURL = self.url + endpoint
		try:
			response = requests.get(fullURL)
			response.raise_for_status()
			data = response.json()
			return data
		except requests.exceptions.RequestException as e:
			log.error("The server couldn\'t fulfill the request.")
			log.error(f"Error code: {e}")


class CardLibrary:
	def __init__(self) -> None:
		self.api = HearthstoneAPI()
		self.load()

	def load(self):
		res = self.api.get()
		assert res is not None
		self.db = res

	def findCard(
			self, identifier: int | str, param: str, multiple: bool = False
	) -> list | dict | None:
		if multiple:
			cardlist = [item for item in self.db if item[param] == identifier]
		else:
			cardlist = next(
				(item for item in self.db if item[param] == identifier), None
			)
		return cardlist

	def formatCard(self, cardstring: str) -> str:
		if "’" in cardstring:
			cardstring = cardstring.replace("’", "'")
		LITTLE_WORDS = ["a", "an", "and", "for", "in", "of", "on", "the", "to"]
		card = " ".join(
			w.capitalize() if w not in LITTLE_WORDS else w for w in cardstring.split()
		)
		return card

	def processCard(self, card: dict) -> dict:
		# Convert any lists into strings
		card = {
			key: ", ".join(value) if isinstance(value, list) else value
			for key, value in card.items()
		}
		# Clean up some strings for display
		if "cost" in card:
			card["cost"] = f"{card['cost']} mana"
		if card["type"] == "WEAPON":
			card["stats"] = f"{card['attack']} attack, {card['durability']} durability."
		elif card["type"] == "LOCATION":
			card["stats"] = f"{card['durability']} durability."
		elif card["type"] == "MINION":
			card["stats"] = f"{card['attack']} attack, {card['health']} health."
		else:
			card["stats"] = None
		card["text"] = self.formatCardText(card["text"])
		keyOrder = [
			"name",
			"cost",
			"stats",
			"text",
			"type",
			"spellSchool",
			"races",
			"cardClass",
			"rarity",
			"set",
			"flavor",
			"mechanics",
			"artist",
		]
		return {k.title(): card[k] for k in keyOrder if k in card and card[k] is not None}

	def displayCard(self, cardData) -> str:
		card = self.processCard(cardData)
		cardstring = []
		for k, v in card.items():
			cardstring.append(f"<p>{k}: {v}</p>")
		return "\n".join(cardstring)

	def formatCardText(self, text: str) -> str:
		return re.sub('<[^<]+?>', '', text)
	
	def listSets(self) -> list:
		setlist = []
		setlist = [[v for k, v in i.items() if k == "set" and v not in setlist] for i in self.db]
		return setlist
