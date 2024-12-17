from dataclasses import replace

import requests
import bs4
import re


PARSING_TEMPLATES =[
        # SERVICE CARD TAG | SERVICE ID | AVERAGE TIME  (FORMAT = (elemProperty, elemPropertyName)
        {
            'service_card': ('tr', {'class': 'servicescategory'}),
            'service_id': ('span', {'class': 'ser-id'}),
            'average_time': ('td', {'class': 'nowrap'}),
            'parsingStyle': ''
        }, {
            'service_card': ('td', {'class': 'whitespace-nowrap'}),
            'service_id': ('a', {'class': 'hover:text_primary'}),
            'average_time': ('div', {'class': 'text-xs'}),
            'parsingStyle': 'firstisid'
        }, {
            'service_card': ('tr', {'data-filter-table-category-id': True}),
            'service_id': ('td', {'data-label': 'ID'}),
            'average_time': ('td', {'class': 'nowrap'}),
            'parsingStyle': ''
        }, {
            'service_card': ('tr', {'data-filter-table-category-id': True}),
            'service_id': ('div', {'class': 'idbutt'}),
            'average_time': ('td', {'class': 'nowrap'}),
            'parsingStyle': ''
        }, {
            'service_card': ('div', {'data-template': 'service'}),
            'service_id': ('div', {'class': 'service-item--id'}),
            'average_time': ('span', {'class': 'badge-danger'}),
            'parsingStyle': 'deletespaces'
        }, {
            'service_card': ('div', {'class': 'tservices-row'}),
            'service_id': ('div', {'data-filter-table-service-id': True}),
            'average_time': ('div', {'class': 'tservice-avt'}),
            'parsingStyle': 'deletespaces'
        }, {
            'service_card': ('tr', {'class': 'divide-x'}),
            'service_id': ('span', {'data-filter-table-service-id': True}),
            'average_time': ('span', {'class': re.compile("|".join(['text-green-600', 'text-blue-600', 'text-red-600', 'text-yellow-600']))}),
            'parsingStyle': ''
        }, {
            'service_card': ('tr', {'data-filter-table-category-id': True}),
            'service_id': ('td', {'data-filter-table-service-id': True}),
            'average_time': ('td', {'class': 'nowrap'}),
            'parsingStyle': ''
        }, {
            'service_card': ('tr', {'data-filter-table-category-id': True}),
            'service_id': ('td', {'data-filter-table-service-id': True}),
            'average_time': ('td', {'class': 'nowrap'}),
            'parsingStyle': ''
        }, {
            'service_card': ('tr', {}),
            'service_id': ('span', {'id': 'servis_id'}),
            'average_time': ('td', {'data-th': 'Gönderim Hızı'}),
            'parsingStyle': ''
        }, {
            'service_card': ('div', {'class': 'service-item'}),
            'service_id': ('span', {'class': 'sp-serv-sm'}),
            'average_time': ('div', {'data-title': 'Average time'}),
            'parsingStyle': 'deletespaces'
        }, {
            'service_card': ('tr', {'class': 'serviceData'}),
            'service_id': ('td', {'data-title': 'ID'}),
            'average_time': ('td', {'data-title': 'Average Time'}),
            'parsingStyle': ''
        }, {
            'service_card': ('div', {'class': 'service-card'}),
            'service_id': ('div', {'class': 'service-card--id'}),
            'average_time': ('span', {'class': 'badge--text'}),
            'parsingStyle': 'splitby2dot'
        }, {
            'service_card': ('tr', {}),
            'service_id': ('td', {}),
            'average_time': ('td', {'class': 'nowrap'}),
            'parsingStyle': ''
        }, {
            'service_card': ('tr', {'class': 'sira'}),
            'service_id': ('td', {'data-title': 'ID'}),
            'average_time': ('td', {'data-title': 'Ort. Tamamlanma Süresi'}),
            'parsingStyle': 'deletespaces'
        }, {
            'service_card': ('tr', {}),
            'service_id': ('td', {'data-title': 'ID'}),
            'average_time': ('td', {'data-title': 'Tamamlanma Süresi'}),
            'parsingStyle': 'deletespaces'
        }, {
            'service_card': ('tr', {'class': 'serviceData'}),
            'service_id': ('td', {'class': 'pm-ikon'}),
            'average_time': ('td', {'data-title': 'Ortalama süre'}),
            'parsingStyle': 'firstisid'
        }, {
            'service_card': ('div', {'class': 'select-service'}),
            'service_id': ('span', {'data-filter-table-service-id': True}),
            'average_time': ('span', {'style': True}),
            'parsingStyle': 'lastisid'
        },
    ]



class AverageTimeParser:
    templates = PARSING_TEMPLATES

    def __init__(self):
        self.parsingResult = {}

    def parse(self, URL) -> bool:
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.89 Safari/537.36'})

        content = None
        try: 
            content = session.get(URL, verify=False)
        except Exception as err:
            print(f'Ошибка при запросе на atime, ', err)
            return False
        
        if content is not None and content.status_code != 200:
            print(content.status_code)
            return False

        soup = bs4.BeautifulSoup(content.text, 'lxml')

        isParsed = False

        for template in self.templates:
            serviceCards = soup.findAll(template['service_card'][0], attrs=template['service_card'][1])

            if len(serviceCards) > 0:
                for serviceCard in serviceCards:
                    serviceId = serviceCard.find(template['service_id'][0], attrs=template['service_id'][1])
                    serviceAverageTime = serviceCard.find(template['average_time'][0], attrs=template['average_time'][1])

                    if serviceId and serviceAverageTime:
                        serviceId = serviceId.text
                        serviceAverageTime = serviceAverageTime.text

                        if 'firstisid' in template['parsingStyle']:
                            serviceId = serviceId.split(' ')[0]

                        if 'lastisid' in template['parsingStyle']:
                            serviceId = serviceId.split(' ')[-1]

                        if 'deletespaces' in template['parsingStyle']:
                            serviceId = serviceId \
                                .replace('  ', '') \
                                .replace('\n', '')

                            serviceAverageTime = serviceAverageTime \
                                        .replace('  ', '') \
                                        .replace('\n', '')

                        if 'splitby2dot' in template['parsingStyle']:
                            try: serviceId = serviceId.split(': ')[1]
                            except: pass

                        self.parsingResult[int(serviceId)] = serviceAverageTime

                        isParsed = True

                if isParsed: break


        return True


def main():
    aTimeParser = AverageTimeParser()
    aTimeParser.parse('https://sosyalize.com/services')

    # tested on
    # https://dripfeedpanel.com/services
    # https://smmperfect.com/services
    # https://spotsocials.com/services
    # https://smm-heaven.net/services
    # https://privatesmm.com/services
    # https://zyadat.com/en/services
    # https://sosyalatom.com/services
    # https://eduofans.com/services
    # https://smmxl.com/services
    # https://instasepeti.com/services
    # https://fbytb.com/services
    # https://bulkcheapservice.com/services
    # https://instantpanel.net/services
    # https://smmtube.pro/services
    # https://likemon.co.kr/services
    # https://smmbro.com/services
    # https://ytmatikvip.com/services
    # https://osemgroupfollowers.com/services
    # https://aysocialmedia.com/services
    # https://paneloji.com/services
    # https://viasmm.com/services
    # https://smmpanel.net/services
    # https://fiverr99.com/services
    # https://klavuzmedya.com/services
    # https://sosyalabone.com/services
    # https://socialpanel.app/en/services
    # https://takipdeposu.com/services
    # https://likecobra.com/services
    # https://sosyalbayin.com/services
    # https://thundersmmpanel.com/services
    # https://medyapanelim.com/services





if __name__ == '__main__':
    main()