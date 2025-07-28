import requests
import hashlib


def parse():
    url = 'https://hh.kz/shards/vacancy/search?items_on_page=50&L_save_area=true&hhtmFrom=vacancy_search_filter&enable_snippets=false&professional_role=96&search_field=name&search_field=company_name&search_field=description&work_format=REMOTE&text=Python'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
    }

    data = []

    params = {
        'items_on_page': 50,
        'hhtmFrom': 'vacancy_search_filter',
        'enable_snippets': 'false',
        'professional_role': 96,
        'search_field': ['name', 'company_name', 'description'],
        'work_format': 'REMOTE',
        'text': 'Python' 
    }


    try:
        response = requests.get(url, headers=headers, params=params)

        response.raise_for_status()

        api_data = response.json()

        vacancies_search = api_data['vacancySearchResult']

        vacancies = vacancies_search.get('vacancies', [])

        for card in vacancies:

            title = card['name']

            company = card['company']['name']

            price_find = card['compensation'].get('to', None)

            if not price_find:
                price = 'Нет цены'
            else:
                price = price_find

            string = f'{title}{company}{price}'

            job_hash = hashlib.md5(string.encode('utf-8')).hexdigest()

            data.append(
                {
                    'job_hash': job_hash,
                    'title': title,
                    'source': 'hh',
                    'price': price,
                    'additionally': f'Компания: {company}'
                }
            )
        
        return data

    except Exception as e:
        print(f'Ошибка: {e}')