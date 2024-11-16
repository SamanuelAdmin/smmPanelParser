from abc import abstractmethod, ABC

class ICurrencyRatesParser(ABC):
	@abstractmethod
	async def parse(self, currency_code: str) -> float | None:
		pass

class CurrencyRatesParser(ICurrencyRatesParser):
	def __init__(self, api_client):
		self.api_client = api_client
	
	def parse(self, currency_code: str) -> float | None:
		'''
		Парсинг передоваемой валюты
		
		:param currency_code: Код валюты, например: 'USD' или 'EUR'
		:return: Значение курса валюты в рублях, деленное на номинал
		'''

		# Получаем список валют и их курс в рублях (например: uds=90rub)
		currencies_json = self.api_client.get_currency_rates()
		if not currencies_json.success and not currencies_json.data:
			raise ValueError('Не удалось получить список валют')
		
		valute_info = currencies_json.data['Valute'].get(currency_code)
		if valute_info is None:
			raise ValueError(f"Валюта {currency_code} не найдена в данных.")

		rate = float(valute_info['Value'])
		nominal = int(valute_info['Nominal'])
		return float(rate / nominal)
	
