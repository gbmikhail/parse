import time
from pprint import pprint

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

LOGIN = '0'          # Example: example@mail.ru
PASSWD = '0'         # Example: qwerty

assert LOGIN and PASSWD, 'Логин и пароль должны быть заполнены'

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru/')

# Авторизация
login = driver.find_element_by_xpath('//input[@name="login"]')
login.send_keys(LOGIN.split('@')[0])
login.send_keys(Keys.ENTER)

time.sleep(1)

passwd = driver.find_element_by_xpath('//input[@type="password"]')
passwd.send_keys(PASSWD)
passwd.send_keys(Keys.ENTER)

# wait
list_wait = WebDriverWait(driver, 15)
list_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')))

mail_links = set()
# Scrolling
while True:
    mail_links_len = len(mail_links)
    links = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')

    for link in links:
        mail_links.add(link.get_attribute('href'))

    actions = ActionChains(driver)
    actions.move_to_element(links[-1])
    actions.perform()

    if len(mail_links) == mail_links_len:
        break

client = MongoClient('127.0.0.1', 27017)
db = client['mail']
mail_collection = db['mail.ru']

# Перебираем письма
for n, link in enumerate(mail_links, 1):
    driver.get(link)

    loading_wait = WebDriverWait(driver, 10)
    tag_from = loading_wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact')))
    data = {
        'link': link,
        'folder': 'Входящие',
        'to': LOGIN,
        'from': tag_from.get_attribute('title'),
        'from_label': tag_from.text,
        'title': driver.find_element_by_xpath('//h2[@class="thread__subject"]').text,
        'date': driver.find_element_by_xpath('//div[@class="letter__date"]').text,
        'content': driver.find_element_by_xpath('//div[@class="letter-body__body"]').text,
    }

    mail_collection.update_one(
        {'link': data['link']},
        {'$set': data},
        upsert=True)

    print(f'> {n} из {len(mail_links)}: {data["title"]}')
print('Готово')
