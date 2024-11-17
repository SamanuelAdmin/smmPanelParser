from abc import ABC, abstractmethod
import requests

from .fetch_result import FetchResult



class IPanelApiClient(ABC):
    @abstractmethod
    def setSession(self, session: requests.Session) -> None:
        """
        Устанвливает сессию для дальнейших запросов
        
        :param session: requests.Session
        
        :return: None
        """
        pass

    @abstractmethod
    def updateHeaders(self, headers: dict) -> None:
        """
        Обновляет заголовки сессии

        :param headers: заголовки в виде {'ключ': 'значение'}

        :return: None
        """
        pass

    @abstractmethod
    def get(self, url: str) -> FetchResult:
        '''
        Запрос на страницу по url(для average time)
        '''
        pass

    @abstractmethod
    def get_info(self, url: str, key: str, action: str) -> FetchResult:
        """
        Получает данные по API относительно указанного параметра action

        :param url: str
        :param key: str
        :param action: balance - получает баланс аккаунта, services - получает список услуг панели

        :return: FetchResult
        """
        pass


class ICurrencyRateApiClient(ABC):
    @abstractmethod
    def get_currency_rates(self) -> FetchResult:
        """
		Получение стоимости валюты в рублях
		Например: в одном долларе 91.1868 рублей
        """
        pass


class PanelApiClient(IPanelApiClient):
    def __init__(self):
        self.session = None

    def setSession(self, session: requests.Session):
        self.session = session
        return self
    
    def updateHeaders(self, headers: dict):
        if self.session:
            self.session.headers = headers
    
    def get(self, url: str) -> FetchResult:
        assert self.session is not None

        try:
            res = self.session.get(url)
            if res.status_code == 200:
                return FetchResult(True, res)
        except requests.exceptions.InvalidURL:
            return FetchResult(False, error=f'Неправильный url {url}', type_error='get for average time')
        except Exception as err:
            return FetchResult(False, error=err, type_error='get for average time')

    def get_info(self, url: str, key: str, action: str) -> FetchResult: # POST request
        assert self.session is not None

        url += 'api/v2'
        params = {
            'key': key,
            'action': action
        }

        if not 'https://' in url:
            return FetchResult(
                False, error=f'\nUrl: {url}\nKey: {key}\nAction: {action}\nError: ошибка в url, не хвататет протокола https'
            )

        try:
            response = self.session.post(url=url, params=params)
        except requests.exceptions.InvalidURL:
            return FetchResult(False, error=f'\nUrl: {url}\nKey: {key}\nAction: {action}\nError: неправильный url')
        except requests.exceptions.MissingSchema:
            return FetchResult(False, error=f'\nUrl: {url}\nKey: {key}\nAction: {action}\nError: ошибка в url')
        except requests.exceptions.ConnectionError as err:
            if 'Name or service not known' in str(err):
                return FetchResult(
                    False, error=f'\nUrl: {url}\nKey: {key}\nAction: {action}\nError: не может найти такой домен'
                )

            return FetchResult(
                False, error=f'\nUrl: {url}\nKey: {key}\nAction: {action}\nError: не известная ошибка {err}'
            )
        else:
            try:
                if response.status_code == 200 or response.status_code == 401:
                    data = response.json()
                    return FetchResult(True, data, status=response.status_code)

                return FetchResult(
                    False, error=f'\nUrl: {url}\nKey: {key}\nAction: {action}\nError: статус код ответа - {response.status_code}'
                )
            except Exception as err:
                return FetchResult(False, error=f'\nUrl: {url}\nKey: {key}\nAction: {action}\nError: {err}')


class CurrencyApiClient(ICurrencyRateApiClient):
    def __init__(self, session: requests.Session):
        self.url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        self.session = session

    def get_currency_rates(self) -> FetchResult:
        try:
            response = self.session.get(url=self.url)

            data = response.json()
            return FetchResult(True, data)
        except Exception as err:
            return FetchResult(False, error=f'Get currency rates error\nError: {err}')
