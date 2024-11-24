from abc import abstractmethod, ABC


class IPanelServicesParser(ABC):
	@abstractmethod
	def parse(self, url: str, key: str) -> list[dict] | None:
		pass


class PanelServicesParser(IPanelServicesParser):
	def __init__(self, api_client):
		self.api_client = api_client

	def parse(self, url: str, key: str) -> list[dict] | None:
		services_data = self.api_client.get_info(url, key, 'services')
		if not services_data.success:
			raise ValueError(f'Не удалось получить сервисы панели {url}')
		
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
						'id': id_ser,
						'name': name_ser,
						'url': url,
						'max': max_ser,
						'min': min_ser,
						'price': price_ser,
					}
				)
			except KeyError:
				print('Ошибка в структуре сервиса')
				continue
		return parsed_data