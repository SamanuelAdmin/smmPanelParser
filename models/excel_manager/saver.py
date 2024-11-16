from abc import ABC, abstractmethod

import os
from idlelib.window import add_windows_to_menu

import xlsxwriter
from PySide6.QtCore import Signal, QThread
from xlsxwriter.worksheet import Worksheet


class ISaverServices(ABC):
    @abstractmethod
    def save(self, services: list[list[dict]], path: str) -> None:
        pass

    def _write_service(self, service: dict, worksheet: Worksheet) -> None:
        pass


class ISpliterServices(ABC):
    @abstractmethod
    def split(self, services: list[dict], max_count: int, sorting: bool = True) -> list[list[dict]]:
        pass


class ServicesSpliter(ISpliterServices):
    def split(self, services: list[dict], max_count: int, sorting: bool = True) -> list[list[dict]]:
        if sorting:
            services = sorted(services, key=lambda x: float(x["currency_to_usd"]))

        service_counter = 0
        res = []
        spliting_services = []
        for service in services:
            spliting_services.append(service)
            service_counter += 1
            if service_counter == max_count:
                res.append(spliting_services)
                spliting_services = []
                service_counter = 0

        if spliting_services: res.append(spliting_services)
        return res


class ServicesSaver(QThread):
    on_save = Signal()
    complete = Signal()

    def __init__(self):
        super().__init__()
        self.row_num = 1
        self.columns = ['id', 'name', 'url', 'max', 'min', 'price', 'currency', 'currency_to_usd', 'dns']

        self.services: list[list[dict]] = None
        self.savingPath: str = None

    def setServices(self, services: list[list[dict]]):
        self.services = services
        return self

    def setSavingPath(self, path: str):
        self.savingPath = path
        return self

    def save(self) -> None:
        file_c = 0

        for service_list in self.services:
            self.row_num = 1

            file_c += 1
            filename = f'save({file_c})_{str(service_list[0]["currency_to_usd"]).replace(".", "_")}.xlsx'
            full_path = os.path.join(self.savingPath, filename)


            workbook = xlsxwriter.Workbook(full_path)
            worksheet = workbook.add_worksheet()
            col_num = 0

            for column in self.columns:
                worksheet.write(0, col_num, column)
                col_num += 1

            for service in service_list:
                self._write_service(service, worksheet)

            workbook.close()
            del workbook, worksheet
            self.services.remove(service_list)

            print(f'[+] SAVE {full_path}')
            self.on_save.emit()

    def _write_service(self, service: dict, worksheet: Worksheet) -> None:
        for col_num, column in zip(range(0, len(self.columns) + 1), self.columns):
            worksheet.write(self.row_num, col_num, service[column])

        self.row_num += 1

    def run(self):
        assert self.services and self.savingPath

        self.save()
        self.complete.emit()