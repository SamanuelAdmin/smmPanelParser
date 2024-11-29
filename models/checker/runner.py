from abc import abstractmethod

from PySide6.QtCore import QThread, Signal
from abc import ABC, abstractmethod

from .checker import PanelPerfomanceChecker
from .checker_manager import CheckerManager

import copy


class ICheckResultSaver(ABC):
    @abstractmethod
    def add(self, **data: dict) -> None: pass

    @abstractmethod
    def save(self) -> None: pass


class CheckerRunner(QThread):
    сompletion = Signal()
    progress = Signal()

    def __init__(
            self, databaseService, panelApiClient,
            checkResultSaver: ICheckResultSaver=None
    ):
        super().__init__()
        self.mode_func = None
        self.panels = None

        self.databaseService = databaseService
        self.panelApiClient = panelApiClient

        self.checkResultSaver = checkResultSaver


    def startChecker(self):
        checker = PanelPerfomanceChecker(self.panelApiClient)

        manager = CheckerManager(
            self.databaseService, checker,
            checkResultSaver=self.checkResultSaver
        )

        if self.mode_func == 'work':
            for _ in manager.startCheckingPanelsWork(self.panels):
                self.progress.emit()
        elif self.mode_func == 'key':
            for _ in manager.startCheckingPanelsKey(self.panels):
                self.progress.emit()
        else:
            raise Exception('Невыбран тип проверки')

    def run(self):
        self.startChecker()
        self.сompletion.emit()
