import requests
from bs4 import BeautifulSoup
import time


login = 'NikiPauk'
password = '1a2b3c4d5e6f7g'

def check_day():
    oneday = 86400
    today = time.gmtime(time.time())
    week_day = time.strftime('%w', today)
    if week_day == '6':
        day = time.gmtime(time.time() + 2*oneday)
        return time.strftime('%d.%m.%y', day)
    else:
        day = time.gmtime(time.time() + 1*oneday)
        return time.strftime('%d.%m.%y', day)

def get_content(date):
    data = {'UserName': login, 'Password': password}
    pars = {'dalykoId': '0',
        'atlikimoData': '30.11.2020'}
    pars1 = {
    'ReturnUrl': '/Darbai/NamuDarbai?dalykoId=0&atlikimoData=' + date}
    url1 = 'https://app.moiashkola.ua/Darbai/NamuDarbai?dalykoId=0&atlikimoData=' +  date
    url3 = 'https://app.moiashkola.ua/?ReturnUrl=%2FDarbai%2FNamuDarbai%3FdalykoId%3D0%26atlikimoData%3D' + date
    s = requests.Session()
    s.post(url=url1, data=data, params=pars)
    r = s.post(url3, data=data, params=pars1)
    return r.text
def get_hw(choosen_day):
    output = 'Домашнє завдання на   ' + choosen_day + '\n' + '\n'
    soup = BeautifulSoup(get_content(choosen_day), 'lxml')
    lessons_tr = soup.find('div', class_='table-responsive').find('table', class_='table border').find_all('tr')
    lessons_tr.pop(0)
    output_list = []
    for lesson in lessons_tr:
        lessons_td = lesson.find_all('td')
        '\r'
        lesson_name = lessons_td[1].get_text().replace('\n', '').replace('', ''). replace('                       ', '').replace('                    ', '  --  ')
        lesson_content = lessons_td[3].get_text().replace('\n', '').replace('\r', '').replace('\xa0', '')
        uroki = ['Сьомий урок', 'Другий урок', 'Перший урок', 'Третій урок', 'Шостий урок', 'П’ятий урок', 'Четвертий урок']
        for urok in uroki:
            lesson_name = lesson_name.replace(urok, '')
        output_list.append(lesson_name + ' ' + lesson_content)
    for lesson_ in output_list:
        output += u'\U000000B7' + lesson_ + '\n' + '\n'
    return output
