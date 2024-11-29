from models.database_service import DatabaseService

from config import parser_service_columns


class Saver:
	def __init__(self, databaseServices: DatabaseService):
		self.databaseServices = databaseServices

	def __update_service(self):
		pass

	def __add_service(self, service):
		pass

	def save(self, services: list[dict]):
		for parsed_service in services:
			print(parsed_service)
			data = self.databaseServices.get_service_by(url=parsed_service['url'], service_id=parsed_service['service_id'])
			if not data:
				self.databaseServices.add_service(parsed_service)
			else:
				# data = [(id, service_id, url, name, max, min, price, currency, currency_to_usd, dns, atime, balance), ...]
				
				service = data[0]
				service_id = service[1]
				name, max, min, price, atime, balance = (service[3], service[4], service[5], service[6], service[10], service[11])

				if name != parsed_service['name']:
					print(f'У {service_id} изменился name с {name} на {parsed_service["name"]}')
				if max != parsed_service['max']:
					print(f'У {service_id} изменился max с {max} на {parsed_service["max"]}')
				if min != parsed_service['min']:
					print(f'У {service_id} изменился min с {min} на {parsed_service["min"]}')
				if price != parsed_service['price']:
					print(f'У {service_id} изменился price с {price} на {parsed_service["price"]}')
				if parsed_service.get('average_time') and atime != parsed_service['average_time']:
					print(f'У {service_id} изменился average_time с {atime} на {parsed_service["average_time"]}')
				if parsed_service.get('balance') and balance != parsed_service['balance']:
					print(f'У {service_id} изменился balance с {balance} на {parsed_service["balance"]}')