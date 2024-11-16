from PySide6.QtCore import QThread, Signal
import requests

from models.parser.currency_converter import CurrencyConverter, ICurrencyConverter
from models.parser.dns import DnsGetter, IDnsGetter
from models.parser.parser_currency import CurrencyRatesParser
from models.parser.parser_panel_currency import PanelCurrencyParser, IPanelCurrencyParser
from models.parser.parser_services import PanelServicesParser, IPanelServicesParser



def add_usd_amount(currency_converter: ICurrencyConverter, currency_code: str, amount: float, service: dict):
	converted_currency = currency_converter.convert(currency_code, amount)
	service['currency_to_usd'] = converted_currency

def usd_add_to_json(currency_converter: ICurrencyConverter, parsed_services: list[dict]):
	for service in parsed_services:
		add_usd_amount(currency_converter, service['currency'], service['price'], service)

	return parsed_services

def currency_panel_add_to_json(parsed_services: list[dict], currency_code: str):
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
		currency_converter: ICurrencyConverter,
		dns_getter: IDnsGetter
	):
	url = url.strip()
	key = key.strip()

	try:
		currency_code_panel = parser_currency_panel.parse(url, key)
	except Exception as err:
		print(err)
		raise err

	services = parser_services.parse(url, key)

	services = currency_panel_add_to_json(services, currency_code_panel)
	services = usd_add_to_json(currency_converter, services)
	services = dns_add_to_json(services, dns_getter)

	return services


class ParsingManager(QThread):
	progress = Signal()
	complete = Signal(list)

	def __init__(self, panels: list[tuple], panelApiClient, currencyApiClient) -> None:
		super().__init__()

		self.panelsForParsing: list[tuple] = panels
		self.panelApiClient = panelApiClient
		self.currencyApiClient = currencyApiClient


	def main(self):
		resultInfo = []
		currency_cache = dict()
		dns_cache = dict()


		parser_currency_panel = PanelCurrencyParser(self.panelApiClient)
		parser_services = PanelServicesParser(self.panelApiClient)
		currency_parser = CurrencyRatesParser(self.currencyApiClient)

		rate_usd = currency_parser.parse('USD')

		currency_converter = CurrencyConverter(currency_parser, currency_cache, rate_usd)

		dns_getter = DnsGetter(dns_cache)

		for panel in self.panelsForParsing:
			panel_id, url, key, is_work, is_work_key = panel

			if not url or not key: continue

			r = parse(url, key, parser_currency_panel, parser_services, currency_converter, dns_getter)
			resultInfo.extend(r)
			self.progress.emit()

		# returning result (panels info)
		self.complete.emit(resultInfo)

	def run(self):
		self.main()