import requests
import re
from pprint import pprint


def get_request(data):
    query = data['query']
    page = data['page']
    region = data['region']
    per_page = 5

    params = {
        'text': query,
        'per_page': per_page,
        'page': page
    }
    if region:
        params['area'] = region

    url = f'https://api.hh.ru/vacancies'

    response = requests.get(url, params=params).json()
    s = ''
    for item in response['items']:
        s += f"<b>Работодатель:</b> {item['employer']['name']}" + '\n'
        s += f"<b>Позиция:</b> {item['name']}" + '\n'
        s += '<b>Требования:</b> ' + replace_highlight_text(item['snippet']['requirement']) + '\n'
        # s += '<b>Обязанности:</b> ' + replace_highlight_text(item['snippet']['responsibility']) + '\n'
        s += f"<i><b>Подробнее о вакансии:</b></i> /getvac_{item['id']}\n\n"

    return response['found'], response['pages'], s


def get_vac(id_vac):
    url_vac_id = f'https://api.hh.ru/vacancies/{id_vac}?host=hh.ru'
    response = requests.get(url_vac_id).json()

    if 'errors' in response:
        return 'Ошибка номера вакансии'

    vac = []
    try:
        vac.append(f"<b>Работодатель:</b> {replace_highlight_text(response['employer']['name'])}")
        if response['address']:
            vac.append(f"<b>Адрес:</b> {replace_highlight_text(response['address']['raw'])}")
        vac.append(f"<b>Позиция:</b> {response['name']}")
        vac.append('')
        if response['description']:
            vac.append('<b>Описание:</b>')
            vac.append(html_to_text(response['description']))
            vac.append('')
        if response['salary']:
            vac.append(
                '<b>Зарплата:</b>' + ((' от ' + str(response['salary']['from'])) if response['salary']['from'] else '') + \
                ((' до ' + str(response['salary']['to'])) if response['salary']['to'] else '') + \
                ((' ' + str(response['salary']['currency'])) if response['salary']['currency'] else ''))
        if 'employment' in response:
            if response['employment']:
                vac.append(f"<b>Занятость:</b> {response['employment']['name']}")
        if 'schedule' in response:
            if response['schedule']:
                vac.append(f"<b>График:</b> {response['schedule']['name']}")
        if 'experience' in response:
            if response['experience']:
                vac.append(f"<b>Опыт работы:</b> {response['experience']['name']}")
        if 'key_skills' in response:
            if response['key_skills']:
                vac.append('<b>Ключевые навыки:</b>')
                for i in response['key_skills']:
                    vac.append(f"- {i['name']}")
        if 'professional_roles' in response:
            if response['professional_roles']:
                vac.append('<b>Профессиональные роли:</b>')
                for i in response['professional_roles']:
                    vac.append(f"- {i['name']}")
        if 'specializations' in response:
            if response['specializations']:
                vac.append('<b>Специализации:</b>')
                for i in response['specializations']:
                    vac.append(f"- {i['name']}")
        if 'languages' in response:
            if response['languages']:
                vac.append('<b>Знание языков:</b>')
                for i in response['languages']:
                    vac.append(f"- {i['name']}, уровень {i['level']['name']}")
        vac.append('')
        vac.append(f"<b>Ссылка на вакансию:</b> {response['alternate_url']}")
    except Exception as ex:
        # вывод в сыром виде в консоль, если была ошибка в обработке
        pprint(response)
        print()
        print(ex)
        return 'Ошибка при запросе'

    return '\n'.join(vac)


def replace_highlight_text(s):
    return str(s).replace('<highlighttext>', '').replace('</highlighttext>', ''). \
        replace('/', ' / ').replace('<', '&lt;').replace('>', '&gt;')


def html_to_text(html=''):
    result = html.replace('<p>', '').replace('<strong>', '').replace('</strong>', '').replace('</p>', '\n') \
        .replace('<ul>', '').replace('</ul>', '').replace('</li>', '\n').replace('<li>', '- ') \
        .replace('<em>', '● ').replace('</em>', '').replace('<br />', '\n').replace('<br/>', '\n') \
        .replace('<br>', '\n').replace('​', '\n').replace('/', ' / ').replace('<', '&lt;').replace('>', '&gt;')
    result = re.sub(' +', ' ', result)
    result = re.sub('\n+', '\n', result)
    return result
