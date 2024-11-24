from typing import Callable

from models import database_controller


class DatabaseService:
    def __init__(self, databaseController: database_controller.Database):
        self.databaseController = databaseController

    # CRUD METHODS
    def add_panel(self, url: str, api_key: str) -> None: # create
        self.databaseController.add_panel(url, api_key)

    def add_service(self, panel_id: int, service_id: int, 
                    url: str, name: str,
                    max: int, min: int,
                    price: float, currency: str,
                    currency_to_usd: float, dns: str,
                    average_time: str, balance: str
                    ):
        self.databaseController.add_service(panel_id, service_id, 
                                            url, name, 
                                            max, min, 
                                            price, currency, 
                                            currency_to_usd, dns, 
                                            average_time, balance)

    def edit_panel(self, id: int, url: str=None, api_key: str=None, work: bool=None, valid_api_key: bool=None) -> None: # update
        self.databaseController.edit_panel(id, url, api_key, work, valid_api_key)

    def get_panels(self, filterFunc: Callable=None): # read
        if filter is not None:
            return list(filter(filterFunc, self.databaseController.get_panels()))

        return self.databaseController.get_panels()

    def get_panels_by(self, panel_id: int=None, work=False, worked_keys_sites=False):
        if panel_id != None: return self.databaseController.get_panel_by_id(panel_id)[0] # returning tuple
        if work: return self.databaseController.get_panels_by_work()
        elif worked_keys_sites: return self.databaseController.get_panels_by_worked_keys_sites()
        else: raise Exception()

    def delete_panel(self, id: int): # delete
        self.databaseController.delete_panel_by_id(id)