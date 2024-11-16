import dns.resolver

from abc import abstractmethod, ABC

class IDnsGetter(ABC):
	def get (self, url: str) -> str:
		pass

class DnsGetter(IDnsGetter):
	def __init__(self, dns_cache: dict):
		self.dns_cache = dns_cache

	def get(self, url: str) -> str:
		domen = url.split('/')[2]

		if self.dns_cache.get(domen):
			return self.dns_cache[domen]

		answer = dns.resolver.resolve(domen, 'NS')
		res = ', '.join([str(server.target) for server in answer])
		self.dns_cache[domen] = res

		return res