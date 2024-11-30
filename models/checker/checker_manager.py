from PyInstaller.compat import is_win

from models.checker.checker import IPanelPerfomanceChecker
from models.database_service import DatabaseService


class CheckerManager:
<<<<<<< HEAD
    def __init__(
            self, databaseService, checker: IPanelPerfomanceChecker,
            checkResultSaver = None
    ):
=======
    def __init__(self, databaseService: DatabaseService, checker: IPanelPerfomanceChecker):
>>>>>>> origin/search_branch
        self.databaseService = databaseService
        self.checker = checker
        self.checkResultSaver = checkResultSaver

    def startCheckingPanelsKey(self, panels):
        for panel in panels:
            try:
                panel_id, url, key, is_work, is_work_key = panel
                check_result = self.checker.checkKey(url, key)

                if check_result:
                    error_message = f'Ключ {key} работает для {url}'

                    if not is_work_key: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(id=panel_id, work=is_work, valid_api_key=True)

                elif not check_result:
                    error_message = f'Ключ {key} не работает для {url}'

                    if is_work_key: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(id=panel_id, work=is_work, valid_api_key=False)
                else:
                    error_message = f'Не удалось проверить {key} для {url}, что-то не так с сайтом'

                print('[INFO] ' + error_message)
                if self.checkResultSaver:
                    self.checkResultSaver.add(
                        url=url,
                        key=key,
                        isURLCorrect=bool(is_work),
                        isKeyCorrect=bool(check_result),
                        errorMessage=error_message
                    )
            finally:
                yield True

    def startCheckingPanelsWork(self, panels):
        for panel in panels:
            try:
                panel_id, url, key, is_working, is_work_key = panel
                check_result = self.checker.checkWork(url, key)

                error_message = ''

                if check_result:
                    error_message = f'Панель {url} работает'

                    if not is_working: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(id=panel_id, work=True, valid_api_key=is_work_key)

                elif not check_result:
                    error_message = f'Панель {url} не работает'

                    if is_working: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(id=panel_id, work=False, valid_api_key=is_work_key)

                else:
                    error_message = f'Что-то не так, не удалось проверить {url}'

                print('[INFO] ' + error_message)
                if self.checkResultSaver:
                    self.checkResultSaver.add(
                        url=url,
                        key=key,
                        isURLCorrect=bool(check_result),
                        isKeyCorrect=bool(is_work_key),
                        errorMessage=error_message
                    )
            finally:
                yield