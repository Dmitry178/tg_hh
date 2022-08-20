import telebot
import hh_api

# Токен, вписать свой
TOKEN = ''

bot = telebot.TeleBot(TOKEN)

# Словарь с названиями регионов на hh.ru, можно сделать запрос на получение данного словаря на hh.ru,
# либо дополнить и вынести словарь с основными регионами в отдельный файл
regions = {0: 'Все регионы', 1: 'Москва', 2: 'Санкт-Петербург', 3: 'Екатеринбург'}

# Словарь для хранения данных пользователей.
# Здесь хранятся запросы на hh.ru, номер страницы, выданной пользователю, регион поиска, и т.д.
# Можно сделать сохранение в файл (pickle), а при дальнейшем расширении - поместить в SQL
query_data = {}


def get_query(user_id, query=''):
    data = get_data(user_id)
    if not query:
        if not data['query']:
            return False, 'Запрос ещё не введён, введите ваш запрос (например, /query_python)'
    else:
        if query != data['query']:
            put_data(user_id, query=query, page=0)

    found, pages, s = hh_api.get_request(query_data[user_id])
    put_data(user_id, found=found, pages=pages)
    return True, s


@bot.message_handler(commands=['start'])
def process_start_command(message):
    msg = 'Бот запущен. Он умеет делать запросы на hh.ru и выводить результаты постранично. Нажмите /help для помощи.'
    bot.send_message(message.from_user.id, msg)


@bot.message_handler(commands=['help'])
def process_help_command(message):
    msg = 'Команды бота:\n' + \
          '/region <N> - установить регион поиска:\n' + \
          '  <N> - номер региона в hh.ru, например:\n' + \
          '  0 - все регионы,\n  1 - Москва,\n  2 - Санкт-Петербург\n' + \
          '/query <запрос> - новый запрос в hh.ru\n' + \
          '/query - повторить предыдущий запрос в hh.ru\n' + \
          '/next - следующая страница запроса\n' + \
          '/prev - предыдущая страница запроса\n' + \
          '/getvac_<vac> - подробнее о вакансии с ID=<vac>\n\n' + \
          'После команд /query и /region допустимо ставить _ вместо пробела.\n\n' + \
          'Примеры запросов:\n' + \
          '/region_0\n' + \
          '/region_2\n' + \
          '/query_python'
    bot.send_message(message.from_user.id, msg)


def set_region(uid, region):
    msg = ''
    if region:
        try:
            region = int(region)
            if region < 0:
                raise TypeError()
        except ValueError:
            msg = 'Ошибка ввода номера региона'
        except TypeError:
            msg = 'Ошибка, номер региона не должен быть отрицательным'
        else:
            put_data(uid, region=region)
    else:
        data = get_data(uid)
        region = data['region']

    if not msg:
        msg = f'Установлен регион поиска: {region}' + f' ({regions[region]})' if region in regions else ''

    return msg


@bot.message_handler()
def process_message_command(message):
    # msg = 'Неверная команда'
    uid = message.from_user.id
    text = str(message.text)
    msg = ''

    if text.startswith('/getvac_'):
        msg = hh_api.get_vac(text[8:])
        bot.send_message(uid, msg, parse_mode='HTML', disable_web_page_preview=True)
        msg = 'Нажмите /query, чтобы вернуться к списку вакансий'

    if text.startswith('/region'):
        msg = set_region(uid, text[8:])

    if text.startswith('/query') or text == '/next' or text == '/prev':
        if text == '/next':
            data = get_data(uid)
            put_data(uid, page=data['page'] + 1)

        if text == '/prev':
            data = get_data(uid)
            put_data(uid, page=data['page'] - 1)

        has_query, msg = get_query(uid, message.text[7:])
        bot.send_message(uid, msg, parse_mode='HTML')

        if not has_query:
            return

        data = get_data(uid)
        msg = f"Найдено позиций: {data['found']}, страница {data['page'] + 1} из {data['pages']}"
        if data['pages'] > 1:
            msg += ('\n/prev - предыдущая страница' if data['page'] > 0 else '') + \
                   ('\n/next - следующая страница' if data['page'] + 1 < data['pages'] else '')

    if msg:
        bot.send_message(uid, msg)


def get_data(user_id):
    if user_id not in query_data:
        put_data(user_id)
    return query_data[user_id]


def put_data(user_id, **kwargs):
    if user_id not in query_data:
        query_data[user_id] = {}

    for key, value in kwargs.items():
        query_data[user_id][key] = value

    if 'region' not in query_data[user_id]:
        query_data[user_id]['region'] = 0
    if 'query' not in query_data[user_id]:
        query_data[user_id]['query'] = ''
    if 'found' not in query_data[user_id]:
        query_data[user_id]['found'] = 0
    if 'pages' not in query_data[user_id]:
        query_data[user_id]['pages'] = 0
    if 'page' not in query_data[user_id]:
        query_data[user_id]['page'] = 0
