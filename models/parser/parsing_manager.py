from PySide6.QtCore import QThread, Signal
import requests

from models.parser.average_time_parser import AverageTimeParser
from models.parser.currency_converter import CurrencyConverter, ICurrencyConverter
from models.parser.dns import DnsGetter, IDnsGetter
from models.parser.parser_currency import CurrencyRatesParser
from models.parser.parser_panel_currency import PanelCurrencyParser, IPanelCurrencyParser
from models.parser.parser_services import PanelServicesParser, IPanelServicesParser
from models.parser.parser_balance import PanelBalanceParser, IPanelBalanceParser



def add_usd_amount(currency_converter: ICurrencyConverter, currency_code: str, amount: float, service: dict):
	converted_currency = currency_converter.convert(currency_code, amount)
	service['currency_to_usd'] = converted_currency

def balance_add_to_json(parsed_services: list[dict], balance):
	for service in parsed_services:
		service['balance'] = balance
	return parsed_services

def usd_add_to_json(currency_converter: ICurrencyConverter, parsed_services: list[dict]):
	for service in parsed_services:
		add_usd_amount(currency_converter, service['currency'], service['price'], service)

	return parsed_services

def atime_add_to_json(parsed_services: list[dict], average_time: dict):
	for service in parsed_services:
		if int(service['id']) in average_time: service['average_time'] = average_time[int(service['id'])]
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
	):
	url = url.strip()
	key = key.strip()

	try:
		currency_code_panel = parser_currency_panel.parse(url, key)
	except Exception as err:
		print(err)

	services = parser_services.parse(url, key)
	balance = parser_balance.parse(url, key)

	if average_time:
		services = atime_add_to_json(services, average_time)
	services = currency_add_to_json(services, currency_code_panel)
	services = usd_add_to_json(currency_converter, services)
	services = dns_add_to_json(services, dns_getter)
	services = balance_add_to_json(services, balance)

	return services


class ParsingManager(QThread):
	progress = Signal()
	complete = Signal(list)

	def __init__(self, panels: list[tuple], panelApiClient, currencyApiClient) -> None:
		super().__init__()

		self.panelsForParsing: list[tuple] = panels
		self.panelApiClient = panelApiClient
		self.currencyApiClient = currencyApiClient


	# main parser func
	def main(self):
		resultInfo = []
		currency_cache = dict()
		dns_cache = dict()

		parser_currency_panel = PanelCurrencyParser(self.panelApiClient)
		parser_services = PanelServicesParser(self.panelApiClient)
		parser_balance = PanelBalanceParser(self.panelApiClient)
		currency_parser = CurrencyRatesParser(self.currencyApiClient)
		rate_usd = currency_parser.parse('USD')

		currency_converter = CurrencyConverter(currency_parser, currency_cache, rate_usd)

		dns_getter = DnsGetter(dns_cache)
		try:
			for panel in self.panelsForParsing:
				try:
					panel_id, url, key, is_work, is_work_key = panel

					if not url or not key: continue

					try:
						atime_parser = AverageTimeParser(self.panelApiClient)
						average_time_res = atime_parser.parse(url)
						if average_time_res:
							average_time: dict[int, str] | None = average_time_res.parsingResult

							general_result = parse(
								url=url, 
								key=key, 
								parser_currency_panel=parser_currency_panel, 
								parser_services=parser_services, 
								parser_balance=parser_balance, 
								currency_converter=currency_converter, 
								dns_getter=dns_getter, 
								average_time=average_time) # atime
							resultInfo.extend(general_result)
					finally:
						self.progress.emit()
						print('Прогресс парсинга 1')
					# general_result = parse(
					# 	url=url, 
					# 	key=key, 
					# 	parser_currency_panel=parser_currency_panel, 
					# 	parser_services=parser_services, 
					# 	parser_balance=parser_balance, 
					# 	currency_converter=currency_converter, 
					# 	dns_getter=dns_getter)

				finally:
					self.progress.emit()
					print('Прогресс парсинга 2')

			# returning result (panels info)
		finally:
			self.complete.emit(resultInfo)

	def run(self):
		self.main()