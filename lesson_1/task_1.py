# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
import json

import requests

if __name__ == '__main__':
    user = 'gbmikhail'
    url = f'https://api.github.com/users/{user}/repos'
    response = requests.get(url).json()
    for item in response:
        print(f"{item['name']:20} {item.get('description') if item.get('description', None) else ''}")

    with open('response.json', 'w', encoding='utf-8') as file:
        data = json.dumps(response, ensure_ascii=False, indent=4)
        file.write(data)
