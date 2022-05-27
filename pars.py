import requests
from bs4 import BeautifulSoup
import csv

# '''В терминале вызываем библиотеку requests(для того чтобы работать с запросами), BeautifulSoup(разбор
# html страницу), csv - встроена и импортируем библиотеки"""

# Задаем константы'''

CSV = 'deposits.csv'
HOST = 'https://myfin.by/'
URL = 'https://myfin.by/vklady'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}

#''' Константа HOST - наш домен, URL - той страницы которую парсим и заголовки HEADERS (просмотр кода (NETWORK)
# и обновляем страницу - accept и user-agent скопировали''')

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
# """Задаем первую функцию обращения к странице, чтобы получить содержимое страницы, мы бробрасываем в первом параметре url,
# второй параметры = параметры. Пишем запрос r, обращаемя к методу библиотеки get(бробрасываем url, заголовки, и
# параметры. B конце функция возвращает нашу переменную r, в которой будет находится наш объект с html.
# Мы можем запустить нашу функцию по параметрам и должны увидеть что наша функция отработала(get.) и сохраняем (html = ),
# html = get_html(URL)
# print(html)
# Запустили без ошибок, можно ее удалить.
# Далее мы работаем точечно, вытягиваем контент.

#Создаю вторую функцию которая у нас будет получать контент, в ней мы будем получать html.
# Использую второй модуль BeautifulSoup(он поможет распарсить html и получить те элементы страницы, которые нам
# нужны,  пишем переменную soup в которую будем получать объект страницы, обращаемся к BeautifulSoup у которого
# параметры html и к htmp парсеру."""

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='deposits-list-item')
    deposits = []
    # print(items)

# '''После того как мы получаем эти элементы items, нам нужно его их складывать, поэтому мы создаем массив
# в который будем складывать эти данные, сразу он будет пустой, но далее в нащей функции будем запускать цикл for
# который будет пробегаться по этим items.'''

# html = get_html(URL)
# get_content(html.text)
# '''Далее запускаем цикл for который будет наши item разбивать на списки, внутри append записываем те данные
# которые мы будем собирать, становимся на название любой карты и указываем этот класс, затем указываем где мы этот
# класс взяли - элемент item.find(div и class) и используем get_text который вытягивает конкретно текст, и в конце
# for мы будем возвращать список, ссылка link_produkt находится там же и еще тег a в скобках get укажем атрибут href
# для указания ссылки, для названия банка мы ищем картинку img, и указываем ссылку на картинку src'''
    for item in items:
        deposits.append(
            {
                'product-name': item.find('div', class_='deposits-list-item__type').get_text(strip=True),
                'link_product': HOST + item.find('div', class_='deposits-list-item__type').find('a').get('href'),
                'percent': item.find('div', class_='deposits-list-item__rate').get_text(strip=True),
                'brand': HOST + item.find('div', class_='deposits-list-item__logo').find('img').get('src')
            }
        )
    return deposits

#'''Проверяем как работает'''
# html = get_html(URL)
# print(get_content(html.text))
#'''Для того чтобы ссылка была ссылкой копируем HOST + , и не было пробелов в get.text пишем strip=True и в brand
# также'''

#'''4. Последним этапом задаем функцию которая работает с сохранением данных (с параметрами items, и куда
# сохраняем и пишем with open чтобы мы могли открыть файл, используем writer и обращаемяс к классу csv. и к методу
# writer, далее задаем заголовки и запускаем цикл for и в каждой итерации дописываем строку, сначала обращаемся
#к самому item и внутри вставляем ключи.

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название вклада', 'Ссылка на продукт', "Процентная ставка", "Банк (картинка)"])
        for item in items:
            writer.writerow( [item['product-name'], item['link_product'], item['percent'], item['brand']])


#'''3. Функция которая будет объект html = get..., в условном операторе if  проверяем чтобы он был равен 200
# в ином случае будет ошибка. Далее вводим константу PAGENATION (спрашиваем указать количество для парсинга)
# далее мы указываем что это целочисленное значение и .strip' без пробелов. Создаем deposits пустой массив и
# пробросим количество страниц и запускаем цикл от 1 , далее используем форматированную строку f и текст, и
# указываем переменную page. Далее пробрасываем URL и дополнительные параметры , пробрасываем параметр page.
# Складываем информацию методом extend и в списке deposits у нас будут списки со всех страниц, внутри списка
# словари, внутрь get_content принимаем html.text.'''

def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code ==200:
        deposits = []
        for page in range(1, PAGENATION):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            deposits.extend(get_content(html.text))
            save_doc(deposits, CSV)
        pass
    else:
        print('Error')

parser()

#'''Укажем save_doc(deposits, CSV)),
# Запуск'''