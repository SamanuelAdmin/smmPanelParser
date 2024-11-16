from abc import ABC, abstractmethod

from models.parser.parser_currency import ICurrencyRatesParser


class ICurrencyConverter(ABC):
	@abstractmethod
	def convert(self, currency_code: str, amount: float) -> float|None:
		pass

class CurrencyConverter(ICurrencyConverter):
	def __init__(self, currency_parser: ICurrencyRatesParser, currency_cache: dict[str, float], rate_usd: float, currency_to: str = 'USD'):
		self.currency_parser = currency_parser
		self.currency_cache = currency_cache
		self.currency_to = currency_to
		self.rate_usd = rate_usd

	def convert(self, currency_code: str, amount: float) -> float|None:
		'''
		:param currency_code: Валюта(ее код), которую нужно перевести:
		:param amount: Количество этой самой валюты
		'''

		if currency_code == self.currency_to:
			return float(amount)

		if currency_code in self.currency_cache:
			currency_rate = self.currency_cache[currency_code]
		else:
			currency_rate = self.currency_parser.parse(currency_code)
			self.currency_cache[currency_code] = currency_rate

		if currency_rate:
			return round(float(float((float(currency_rate) / float(self.rate_usd))) * float(amount)), 4)
		return None