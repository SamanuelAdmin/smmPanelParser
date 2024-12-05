from models.database_service import DatabaseService

class Saver:
	def __init__(self, databaseServices: DatabaseService):
		self.databaseServices = databaseServices

	def __add_service(self, service: dict) -> None:
		# print()
		self.databaseServices.add_service(service)
		# print(f'Добавил сервис {service["service_id"]}({service["name"]})')
		# print()

	def __update_service(self, new_service: dict, old_service: dict) -> None:
		# print()
		# print(f'Сервис {old_service["service_id"]}:')
		for key, value in new_service.items():
			if key == 'url' or key == 'service_id' or key == 'dns':
				continue

			# print(f'Сверяю {key}({value}) с {old_service[key]} из data')
			if old_service[key] != value:
				self.databaseServices.edit_service(
					{
						key: value,
						'id': old_service['id']
					}
				)
				# print(f'У {old_service["service_id"]} изменился {key} с {old_service[key]} на {value}')
		# print()

	def save(self, services: list[dict]):
		for parsed_service in services:
			try:
				data = self.databaseServices.get_service_by(
					{'url': parsed_service['url'], 'service_id': parsed_service['service_id']}
				)
				if not data: 
					# print('Add:', parsed_service)
					self.__add_service(parsed_service)
				else:
					# print('Edit:', data[0], ' to:', parsed_service)
					self.__update_service(parsed_service, data[0])
			finally:
				yield