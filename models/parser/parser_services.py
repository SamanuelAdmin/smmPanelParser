from abc import abstractmethod, ABC


from models.api_manager.api_client import IPanelApiClient

class IPanelServicesParser(ABC):
	@abstractmethod
	def parse(self, url: str, key: str) -> list[dict] | None:
		pass


class PanelServicesParser(IPanelServicesParser):
	def __init__(self, api_client: IPanelApiClient):
		self.api_client = api_client

	def parse(self, url: str, key: str) -> list[dict] | None:
		services_data = self.api_client.get_info(url, key, 'services')
		if not services_data.success:
			# raise ValueError(f'Не удалось получить сервисы панели {url}')
			print(f'Не удалось получить сервисы панели {url}')
			return None

		parsed_data = []
		for service in services_data.data:
			try:
				id_ser = service['service']
				name_ser = service['name']
				max_ser = service['max']
				min_ser = service['min']
				price_ser = service['rate']
				parsed_data.append(
					{
						'service_id': int(id_ser),
						'url': url,
						'name': name_ser,
						'max': int(max_ser),
						'min': int(min_ser),
						'price': float(price_ser),
					}
				)
			except Exception as err:
				print('Ошибка в структуре сервиса,', err)
				continue
		return parsed_data