from abc import abstractmethod, ABC


class IPanelBalanceParser(ABC):
	@abstractmethod
	def parse(self, url: str, key: str) -> float | None:
		pass


class PanelBalanceParser(IPanelBalanceParser):
	def __init__(self, api_client):
		self.api_client = api_client

	def parse(self, url: str, key: str) -> float | None:
		try:
			balance_data = self.api_client.get_info(url, key, 'balance')
			if not balance_data.success:
				raise ValueError(f'Не удалось получить баланс панели {url}')
		
			return float(balance_data.data['balance'])
		except Exception as err:
			print(err)
			return
		
		