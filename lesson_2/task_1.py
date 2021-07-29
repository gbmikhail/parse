# Вариант 1
# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы
# получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько
# страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
#
#     Наименование вакансии.
#     Предлагаемую зарплату (отдельно минимальную и максимальную).
#     Ссылку на саму вакансию.
#     Сайт, откуда собрана вакансия.
#
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame
# через pandas. Сохраните в json либо csv.
from pprint import pprint

import requests
from bs4 import BeautifulSoup


url = 'https://moskow.hh.ru'
# search = input('Профессия, должность или компания:')
search = 'python'

params = {
    'area': 1,
    'fromSearchLine': True,
    'st': 'searchVacancy',
    'text': search
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.93 Safari/537.36'
}


def get_compensation(value):
    _min = None
    _max = None
    _val = None
    if value:
        if value.split()[0] == 'от':
            _val = ''.join(value.split()[-1:])
            _min = int(value.replace('от', '').replace(f'{_val}', '').replace(' ', ''))
        elif value.split()[0] == 'до':
            _val = ''.join(value.split()[-1:])
            _max = int(value.replace('до', '').replace(f'{_val}', '').replace(' ', ''))
        else:
            _val = ''.join(value.split()[-1:])
            _tmp = value.replace(f'{_val}', '').split()
            _min = int(_tmp[0:1][0])
            _max = int(_tmp[-1:][0])
    return {
        'min': _min,
        'max': _max,
        'val': _val,
    }


def parse(form_url, _params=None):
    response = requests.get(form_url, params=_params, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    pager = soup.find('div', attrs={'data-qa': 'pager-block'})
    next_page = pager.find('a', attrs={'data-qa': 'pager-next'})
    if next_page:
        next_page = next_page.get('href')

    for vacancy in vacancy_list:
        header = vacancy.find('div', attrs={'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})
        title = header.find('a', attrs={'class': 'bloko-link'})
        company = vacancy.find('a', attrs={'class': 'bloko-link bloko-link_secondary'})

        compensation = None
        if len(list(header.children)) > 1:
            compensation = list(header.children)[1].getText().replace('\u202f', '')
        data = {
            'name': title.get_text().replace('\xa0', ' '),
            'link': title.get('href'),
            'company': company.getText().replace('\xa0', ' ') if company else None,
            'compensation': get_compensation(compensation),
            'from': response.url,
        }
        pprint(data)

    return next_page


_next_page = parse(f'{url}/search/vacancy', params)
while _next_page:
    _next_page = parse(f'{url}{_next_page}')
