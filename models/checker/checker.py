from abc import abstractmethod, ABC


class IPanelPerfomanceChecker(ABC):
    @abstractmethod
    async def checkKey(self, url: str, key: str):
        pass

    @abstractmethod
    async def checkWork(self, url: str, key: str):
        pass


class PanelPerfomanceChecker(IPanelPerfomanceChecker):
    def __init__(self, api_client):
        self.api_client = api_client

    def checkKey(self, url: str, key: str) -> bool:
        response = self.api_client.get_info(url, key, 'balance')

        # if response is success and client has been auth
        return response.success == True and response.status != 401

    def checkWork(self, url: str, key: str) -> bool:
        response = self.api_client.get_info(url, key, 'balance')

        if response.success:
            # if request has been valid method will return True
            return 'Invalid' in response.data or 'balance' in response.data

        return False