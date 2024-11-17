import requests

from bs4 import BeautifulSoup
from g4f.client import Client # https://github.com/xtekky/gpt4free/blob/main/docs/async_client.md
import concurrent.futures
import copy


def getPrompt(text):
    return f'''Parse the values in format
SERVICE ID (ONLY NUMBER) - AVARAGE TIME VALUE
every service info will be from the new line
(YOU DONT NEED TO PUT ANY WORDS LIKE "SERVICE ID" IN AN ANSWER EXCEPT NUMBERS)
You cannot use another type of response except this, and you must send only information like this.
Warning! this fields can have another names (or different languages)


EXAMPLE OF AN ANSWER (ITS FOR ONLY 4 SERVICES, BUT YOU NEED TO DO FOR Y`ALL THIS):
6755 - 55 seconds
4565 - 35 seconds
46 - 1 minute
6465- 5 seconds

YOU HAVE TO DO THIS FOR EVERY SERVICE WHICH YOU CAN FIND

Here is a page source code which you need to parse

{text}

Do this parsing for every servise, info about you will find

NOTICE: IF YOU CANNOT FIND ANY SERVICE INFORMATION, JUST SAY "NONE"'''




class AverageTimeParser:
    def __init__(self, session: requests.Session):
        self.parsingResult = {}

        self.session: requests.Session = session
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'})

    def parseTextPart(self, textPart: str):
        self.threadNumber += 1
        currentThreadNumber = self.threadNumber
        print(f'Thread {self.threadNumber} started')

        client = Client(
            # proxies="http://117.54.114.101",
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": getPrompt(textPart)}],
        )

        for line in response.choices[0].message.content.splitlines():
            try:
                serviceNum, aTimeValue = line.split(' - ')
                self.parsingResult[int(serviceNum)] = aTimeValue
            except Exception as e:
                print(currentThreadNumber, response.choices[0].message.content)
                # pass

        self.finishedProcess += 1
        return currentThreadNumber


    def parse(self, URL: str):
        URL += 'en/services'

        response = self.session.get(URL)

        if response.status_code == 200:
            userText: str = BeautifulSoup(response.text, "lxml").get_text(separator="\n", strip=True)

            self.threadNumber = 0
            self.finishedProcess = 0

            # split for parts (20000 symbols in one part)
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                def grouper(iterable, n):
                    args = [iter(iterable)] * n
                    return zip(*args)

                splitedText: list = [
                        ''.join(i) for i in grouper(userText, 20000)
                    ]

                for textPart in splitedText:
                    executor.submit(self.parseTextPart, textPart)

                # waiting until the end
                while self.finishedProcess != len(splitedText): pass

        return self

