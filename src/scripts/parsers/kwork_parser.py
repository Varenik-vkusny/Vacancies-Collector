import requests
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def parse():
    base_url = 'https://kwork.ru/projects?c=41'
    session_cookies = None

    data = []

    chrome_options = Options()
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"Перехожу на {base_url}...")
        driver.get(base_url)

        time.sleep(5)

        session_cookies = driver.get_cookies()

    finally:
        driver.quit()


    if not session_cookies:
        print('Не удалось взять cookies')
        exit()


    session = requests.Session()



    for cookie in session_cookies:
        session.cookies.set(cookie['name'], cookie['value'])


    api_url = f'https://kwork.ru/projects'

    params = {
        'c': 41,
        'page': 1
    }

    payload = {
        'c': 41,
        'page': 1
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': base_url
    }


    try:
        response = session.post(api_url, headers=headers, params=params, data=payload)

        print('Сделал request')

        response.raise_for_status()

        json_data = response.json()

        projects = json_data['data']['wants']

        print(f'Нашел все проекты {len(projects)}')


        for project in projects:

            title = project['name']
            
            description = project['description']

            price = project['priceLimit']

            possible_price = project.get('possiblePriceLimit', 'Нет возможной цены.')

            string = f'{title}{price}{possible_price}'

            job_hash = hashlib.md5(string.encode('utf-8')).hexdigest()

            data.append(
                {
                    'job_hash': job_hash,
                    'title': title,
                    'description': description,
                    'source': 'Kwork',
                    'price': price,
                    'additionally': f'Возможная цена: {possible_price}'
                }
            )

            print('Добавил в дату данные')

        return data

    except Exception as e:
        print(f'Ошибка: {e}')   
        return