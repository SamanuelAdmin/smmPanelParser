from abc import abstractmethod, ABC
from typing import Union

class IPanelCurrencyParser(ABC):
	@abstractmethod
	def parse(self, url: str, key: str) -> str | None:
		'''
		Парсинг валюту панели

		:return: Возвращает код валюты(например: USD или EUR)
		'''
		pass

class PanelCurrencyParser(IPanelCurrencyParser):
	def __init__(self, api_client):
		self.api_client = api_client

	def parse(self, url: str, key: str) -> str | None:
		balance_data = self.api_client.get_info(url, key, 'balance')
		if not balance_data.success and not balance_data.data:
			raise ValueError(f'Не удалось получить данные о балансе панели {url}')
		
		try:
			return balance_data.data['currency']
		except Exception as err:
			raise ValueError(f'Не удалось получить валюту панели {url}\n{err}')