from PyInstaller.compat import is_win

from models.checker.checker import IPanelPerfomanceChecker


class CheckerManager:
    def __init__(self, databaseService, checker: IPanelPerfomanceChecker):
        self.databaseService = databaseService
        self.checker = checker

    def startCheckingPanelsKey(self, panels):
        for panel in panels:
            try:
                panel_id, url, key, is_work, is_work_key = panel
                check_result = self.checker.checkKey(url, key)

                if check_result:
                    print(f'[INFO] ключ {key} работает для {url}')

                    if not is_work_key: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(url, key, panel_id, isWorking=is_work, isKeyValid=True)

                elif not check_result:
                    print(f'[INFO] ключ {key} не работает для {url}')

                    if is_work_key: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(url, key, panel_id, isWorking=is_work, isKeyValid=False)
                else:
                    print(f'[INFO] не удалось проверить {key} для {url}, что-то не так с сайтом')
            finally:
                yield True

    def startCheckingPanelsWork(self, panels):
        for panel in panels:
            try:
                panel_id, url, key, is_working, is_work_key = panel
                check_result = self.checker.checkWork(url, key)

                if check_result:
                    print(f'[INFO] панель {url} работает')

                    if not is_working: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(url, key, panel_id, isWorking=True, isKeyValid=is_work_key)

                elif not check_result:
                    print(f'[INFO] панель {url} не работает')

                    if is_working: # optimisation of queries (to DB)
                        self.databaseService.edit_panel(url, key, panel_id, isWorking=False, isKeyValid=is_work_key)

                else:
                    print(f'[INFO] что-то не так, не удалось проверить {url}')
            finally:
                yield