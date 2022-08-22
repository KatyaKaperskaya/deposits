import requests
from bs4 import BeautifulSoup
import csv

# """In the terminal, we call the  library "requests" (in order to work with requests), "BeautifulSoup" (parsing
# "html" page), csv - built in and import libraries"""

# """Set constants"""

CSV = 'deposits.csv'
HOST = 'https://myfin.by/'
URL = 'https://myfin.by/vklady'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}

#''' The constant "HOST" - is our domain, "URL" - of that page is parsed and "HEADERS" headers (code view (NETWORK)
# and page refresh - "accept" and "user-agent" copied''')

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
# """1. We set the first destination of the page call to get the content of the page, we look in the first parameter of the URL,
# second parameter = parameter. We write a request "r", we turn to method the library "get" (we pick "url", headers, and
# parameter. The B function returns our variable "r", which contains our "html" object.
# We use our function by parameters and should see that our function worked (get.) and saved (html = ).
# html = get_html(URL)
# print(html)
# Launched without errors, you can delete it.
# Next, we work pointwise, pulling out the content.

# 2. I create a second function that will receive content from us, in which we will receive "html".
# I use the second module "BeautifulSoup" (it will help parse "html" and get those page elements that we
# are needed, we write the variable "soup" into which we will receive the page object, we turn to "BeautifulSoup" for which
# "html" parameters and to the "htmp" parser."""

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='deposits-list-item')
    deposits = []
    # print(items)

# '''After we get these "items", we need to add them together, so we create an array
# in which we will add this data, it will immediately be empty, but then in our function we will run the loop "for"
# which will iterate over these "items".'''

# html = get_html(URL)
# get_content(html.text)
# '''Next, we launch the loop "for", which will split our "item" into lists, inside append we write that data
# which we will collect, become the name of any card and indicate this class, then indicate where we are this
# the class was taken - the element "item.find" (div and class) and use "get_text" which pulls out the specific text, and at the end
# "for" we will return a list, the "link_produkt" is in the same place and also the a tag in the brackets "get", specify the attribute "href"
# to specify a link, for the name of the bank we are looking for an image "img", and specify a link to the image "src"'''
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

#'''Checking how it works'''
# html = get_html(URL)
# print(get_content(html.text))
#'''In order for the link to be a link, copy "HOST" + , and there are no spaces in "get.text", write "strip=True" and in the "brand"
# also'''

#'''4. The last step is to set a function that works with saving data (with parameters "items", and where
# save and write "with open" so we can open the file, use "writer" and call the class "csv." and to the method
# "writer", then we set the headers and run the "for" loop and in each iteration we add a line, first we turn
#to the itself "item" and insert the keys inside.

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название вклада', 'Ссылка на продукт', "Процентная ставка", "Банк (картинка)"])
        for item in items:
            writer.writerow( [item['product-name'], item['link_product'], item['percent'], item['brand']])


#'''3. The function that will be the object "html = get..." , in the "if" statement we check that it is equal to 200
# otherwise there will be an error. Next, enter the constant PAGENATION (we ask you to specify the amount for parsing)
# next we specify that this is an integer value and ".strip" without spaces. We create deposits an empty array and
# forward the number of pages and loop from 1 , then use the format string "f" and text, and
# set the variable "page". Next, we forward the "URL" and additional parameters, we forward the parameter "page".
# We add the information using the method "extendand" in the list "deposits" we will have lists from all pages inside the list
# dictionaries, inside "get_content" we accept "html.text".'''
"
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

#'''Specify "save_doc"(deposits, CSV)),
# Run'''
