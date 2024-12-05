from typing import Callable

from models import database_controller


class DatabaseService:
    def __init__(self, databaseController: database_controller.Database):
        self.databaseController = databaseController

    # CRUD METHODS
    def add_panel(self, url: str, api_key: str) -> None: # create
        self.databaseController.add_panel(url, api_key)

    def add_service(self, data: dict):
        self.databaseController.add_service(data)
    
    def edit_service(self, data: dict):
        self.databaseController.edit_service(data)

    def edit_panel(self, id: int, url: str=None, api_key: str=None, work: bool=None, valid_api_key: bool=None) -> None: # update
        self.databaseController.edit_panel(id, url, api_key, work, valid_api_key)

    def get_panels(self) -> list: # read
        return self.databaseController.get_panels()
    
    def get_services(self) -> list[dict]:
        return self.databaseController.get_services()
    
    def get_service_by(self, data: dict) -> None:
        return self.databaseController.get_service_by(data)
    
    def get_panels_by(self, panel_id: int=None, work=None, worked_keys_sites=None):
        if panel_id != None: return self.databaseController.get_panel_by_id(panel_id)[0] # returning tuple

        if work and worked_keys_sites: return self.databaseController.get_panels_by_work_and_valid_key()
        elif work: return self.databaseController.get_panels_by_work()
        elif worked_keys_sites: return self.databaseController.get_panels_by_worked_keys_sites()
        else: raise Exception()

    def delete_panel(self, id: int): # delete
        self.databaseController.delete_panel_by_id(id)