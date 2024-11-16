from typing import Callable

from models import database_controller


class DatabaseService:
    def __init__(self, databaseController: database_controller.Database):
        self.databaseController = databaseController

    # CRUD METHODS
    def add_panel(self, url: str, key: str) -> None: # create
        self.databaseController.add_panel(url, key)

    def get_panels(self, filterFunc: Callable=None): # read
        if filter is not None:
            return list(filter(filterFunc, self.databaseController.get_panels()))

        return self.databaseController.get_panels()

    def get_panels_by(self, panel_id: int=None, work=False, worked_keys_sites=False):
        if panel_id != None: return self.databaseController.get_panel_by_id(panel_id)[0] # returning tuple
        if work: return self.databaseController.get_panels_by_work()
        elif worked_keys_sites: return self.databaseController.get_panels_by_worked_keys_sites()
        else: raise Exception()

    def edit_panel(
            self,
            url: str, api_key: str, id: str,
            isWorking: bool=True, isKeyValid: bool=True
    ) -> None: # update
        self.databaseController.edit_panel(url, api_key, id, isWorking, isKeyValid)

    def delete_panel(self, id: int): # delete
        self.databaseController.delete_panel_by_id(id)