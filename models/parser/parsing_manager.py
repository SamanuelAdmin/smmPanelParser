from cgi import parse_multipart

from PySide6.QtCore import QThread, Signal
import requests

from models.api_manager.api_client import PanelApiClient, CurrencyApiClient
from models.api_manager.user_agent_manager import getRandomUserAgent
from models.parser.average_time_parser import AverageTimeParser
# from models.parser.average_time_parser import AverageTimeParser
from models.parser.currency_converter import CurrencyConverter, ICurrencyConverter
from models.parser.dns import DnsGetter, IDnsGetter
from models.parser.parser_currency import CurrencyRatesParser
from models.parser.parser_panel_currency import PanelCurrencyParser, IPanelCurrencyParser
from models.parser.parser_services import PanelServicesParser, IPanelServicesParser
from models.parser.parser_balance import PanelBalanceParser, IPanelBalanceParser
from models.database_service import DatabaseService
from models.database_controller import Database


def add_usd_amount(currency_converter: ICurrencyConverter, currency_code: str, amount: float, service: dict):
	converted_currency = currency_converter.convert(currency_code, amount)
	if converted_currency:
		service['currency_to_usd'] = float(converted_currency)

def balance_add_to_json(parsed_services: list[dict], balance):
	for service in parsed_services:
		service['balance'] = balance
	return parsed_services

def usd_add_to_json(currency_converter: ICurrencyConverter, parsed_services: list[dict]):
	for service in parsed_services:
		add_usd_amount(currency_converter, service['currency'], service['price'], service)

	return parsed_services

def atime_add_to_json(parsed_services: list[dict], average_time: dict | None):
	for service in parsed_services:
		if int(service['service_id']) in average_time: service['average_time'] = average_time[int(service['service_id'])]
		else: service['average_time'] = ''

	return parsed_services

def currency_add_to_json(parsed_services: list[dict], currency_code: str):
	for service in parsed_services:
		service['currency'] = currency_code

	return parsed_services

def dns_add_to_json(parsed_services: list[dict], dns_getter: IDnsGetter):
	for service in parsed_services:
		url = service['url']
		dns = dns_getter.get(url)
		service['dns'] = dns
	return parsed_services


def parse(
		url: str, key: str,
		parser_currency_panel: IPanelCurrencyParser,
		parser_services: IPanelServicesParser,
		parser_balance: IPanelBalanceParser,
		currency_converter: ICurrencyConverter,
		dns_getter: IDnsGetter,
		average_time=None
	) -> None|list[dict]:
	url = url.strip()
	key = key.strip()

	services = parser_services.parse(url, key)
	if not services: return None

	balance = parser_balance.parse(url, key)

	if average_time:
		services = atime_add_to_json(services, average_time)

	try:
		currency_code_panel = parser_currency_panel.parse(url, key)
		services = currency_add_to_json(services, currency_code_panel)
	except Exception as err:
		print(err)
		return None

	services = usd_add_to_json(currency_converter, services)
	services = dns_add_to_json(services, dns_getter)
	
	if balance is not None and isinstance(balance, float): services = balance_add_to_json(services, balance)
	else: services = balance_add_to_json(services, 'не смог получить')

	return services


class ParsingManager(QThread):
	progress = Signal()
	complete = Signal(list)

	def __init__(self, panels: list[tuple]) -> None:
		super().__init__()

		self.panelsForParsing: list[tuple] = panels


	def generateApiClients(self):
		panelApiClientSession = requests.Session()
		panelApiClientSession.headers.update(
			{
				'User-Agent': getRandomUserAgent(),
			}
		)

		currencyApiClientSession = requests.Session()

		panelApiClient = PanelApiClient().setSession(panelApiClientSession)
		currencyApiClient = CurrencyApiClient( currencyApiClientSession )

		return panelApiClient, currencyApiClient

	# main parser func
	def main(self):
		resultInfo = []
		currency_cache = dict()
		dns_cache = dict()

		# panelApiClient, currencyApiClient = self.generateApiClients()
		#
		# parser_currency_panel = PanelCurrencyParser(panelApiClient)
		# parser_services = PanelServicesParser(panelApiClient)
		# parser_balance = PanelBalanceParser(panelApiClient)
		# currency_parser = CurrencyRatesParser(currencyApiClient)
		# rate_usd = currency_parser.parse('USD')
		# currency_converter = CurrencyConverter(currency_parser, currency_cache, rate_usd)

		# saver_to_database = SaverServices(self.databaseService)

		dns_getter = DnsGetter(dns_cache)


		try:
			for panel in self.panelsForParsing:
				# creating parsers obj
				panelApiClient, currencyApiClient = self.generateApiClients()

				parser_currency_panel = PanelCurrencyParser(panelApiClient)
				parser_services = PanelServicesParser(panelApiClient)
				parser_balance = PanelBalanceParser(panelApiClient)
				currency_parser = CurrencyRatesParser(currencyApiClient)
				rate_usd = currency_parser.parse('USD')
				currency_converter = CurrencyConverter(currency_parser, currency_cache, rate_usd)

				try:
					panel_id, url, key, is_work, is_work_key = panel
					print(f'Идет парсинг {url} {key}')

					if not url or not key: continue

					atime_parser = AverageTimeParser()
					atime_parser.parse(url + 'services')
					average_time_result: dict[int, str] | None = atime_parser.parsingResult
					self.progress.emit()


					general_result = parse(
						url=url,
						key=key,
						parser_currency_panel=parser_currency_panel,
						parser_services=parser_services,
						parser_balance=parser_balance,
						currency_converter=currency_converter,
						dns_getter=dns_getter,
						average_time=average_time_result # atime
					)

					if general_result != None: resultInfo.extend(general_result)

				except Exception as err:
					print(err)
				finally:
					self.progress.emit()

		except Exception as err:
			print(err)
		finally:
			self.complete.emit(resultInfo)

	def run(self):
		self.main()