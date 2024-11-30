import xlsxwriter
from xlsxwriter.worksheet import Worksheet


class CheckResultSaver:
    def __init__(self):
        self.saving_buffer: list[dict] = []

    def add(self, **data) -> None:
        '''
            DATA FORMAT
            {
                'url': URL: str,
                'key': KEY: str,
                'isURLCorrect': True | False,
                'isKeyCorrect': True | False,
                'errorMessage': errorMessage: str
            }
        '''

        self.saving_buffer.append(data)

    def isEmpty(self):
        return len(self.saving_buffer) == 0

    def save(self, fullFilePath: str) -> bool:
        columns = {
            0: ('url', 'URL'),
            1: ('key', 'KEY'),
            2: ('isURLCorrect', 'IS URL CORRECT'),
            3: ('isKeyCorrect', 'IS KEY CORRECT'),
            4: ('errorMessage', 'MESSAGE')
        }

        workbook = xlsxwriter.Workbook(fullFilePath)
        worksheet = workbook.add_worksheet()

        # writing columns
        col_num = 0

        for columnNum, columnData in columns.items():
            worksheet.write(0, columnNum, columnData[1])
            col_num += 1

        # writing services info
        service_num = 1

        for serviceInfo in self.saving_buffer:
            for columnNum, columnData in columns.items():
                worksheet.write(
                    service_num, columnNum,
                    serviceInfo.get(columnData[0])
                )

            service_num += 1

        workbook.close()
        return True