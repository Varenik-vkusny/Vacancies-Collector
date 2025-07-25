import requests
from bs4 import BeautifulSoup


url = 'https://hh.kz/search/vacancy?ored_clusters=true&order_by=publication_time&area=159&search_field=name&search_field=company_name&search_field=description&work_format=REMOTE&text=Python+developer&enable_snippets=false'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
}

data = []

try:
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    vacancies_cards = soup.find_all('div', 'vacancy-info--ieHKDTkezpEj0Gsx')

    for card in vacancies_cards:

        title = card.select_one('#a11y-main-content > div:nth-child(2) > div > div.magritte-card___bhGKz_8-0-1.magritte-card-style-primary___eZ6aX_8-0-1.magritte-card-shadow-level-0___RNbQK_8-0-1.magritte-card-stretched___0Uc0J_8-0-1.magritte-card-press-enabled___kXfCl_8-0-1.magritte-card-hover-enabled___-wolU_8-0-1.magritte-increase-shadow___Lvfmm_8-0-1.magritte-border-default___eT8Lg_8-0-1 > div.magritte-icon-dynamic___KJ4yJ_12-0-0.magritte-icon-dynamic_full-width___vgWH5_12-0-0.magritte-icon-dynamic_hover-enabled___WblhN_12-0-0.magritte-icon-dynamic_press-enabled___aGKHB_12-0-0 > div > div > div > div.vacancy-info--ieHKDTkezpEj0Gsx > h2 > span > a > div > span > span')

        company = card.select_one('#a11y-main-content > div:nth-child(2) > div > div.magritte-card___bhGKz_8-0-1.magritte-card-style-primary___eZ6aX_8-0-1.magritte-card-shadow-level-0___RNbQK_8-0-1.magritte-card-stretched___0Uc0J_8-0-1.magritte-card-press-enabled___kXfCl_8-0-1.magritte-card-hover-enabled___-wolU_8-0-1.magritte-increase-shadow___Lvfmm_8-0-1.magritte-border-default___eT8Lg_8-0-1 > div.magritte-icon-dynamic___KJ4yJ_12-0-0.magritte-icon-dynamic_full-width___vgWH5_12-0-0.magritte-icon-dynamic_hover-enabled___WblhN_12-0-0.magritte-icon-dynamic_press-enabled___aGKHB_12-0-0 > div > div > div > div.vacancy-info--ieHKDTkezpEj0Gsx > div.info-section--YaC_npvTFcwpFd1I > div.narrow-container--HaV4hduxPuElpx0V > a > div > span > span')

        job_format = card.select_one('#a11y-main-content > div:nth-child(2) > div > div.magritte-card___bhGKz_8-0-1.magritte-card-style-primary___eZ6aX_8-0-1.magritte-card-shadow-level-0___RNbQK_8-0-1.magritte-card-stretched___0Uc0J_8-0-1.magritte-card-press-enabled___kXfCl_8-0-1.magritte-card-hover-enabled___-wolU_8-0-1.magritte-increase-shadow___Lvfmm_8-0-1.magritte-border-default___eT8Lg_8-0-1 > div.magritte-icon-dynamic___KJ4yJ_12-0-0.magritte-icon-dynamic_full-width___vgWH5_12-0-0.magritte-icon-dynamic_hover-enabled___WblhN_12-0-0.magritte-icon-dynamic_press-enabled___aGKHB_12-0-0 > div > div > div > div.vacancy-info--ieHKDTkezpEj0Gsx > div:nth-child(8) > div > div:nth-child(2) > div > span')

        price = card.select_one('#a11y-main-content > div:nth-child(3) > div > div.magritte-card___bhGKz_8-0-1.magritte-card-style-primary___eZ6aX_8-0-1.magritte-card-shadow-level-0___RNbQK_8-0-1.magritte-card-stretched___0Uc0J_8-0-1.magritte-card-press-enabled___kXfCl_8-0-1.magritte-card-hover-enabled___-wolU_8-0-1.magritte-increase-shadow___Lvfmm_8-0-1.magritte-border-default___eT8Lg_8-0-1 > div.magritte-icon-dynamic___KJ4yJ_12-0-0.magritte-icon-dynamic_full-width___vgWH5_12-0-0.magritte-icon-dynamic_hover-enabled___WblhN_12-0-0.magritte-icon-dynamic_press-enabled___aGKHB_12-0-0 > div > div > div > div.vacancy-info--ieHKDTkezpEj0Gsx > div:nth-child(8) > span')

        data.append(
            {
                'title': title.text.strip(),
                'source': 'hh',
                'price': price.text.strip()
            }
        )