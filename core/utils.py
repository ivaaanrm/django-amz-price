import lxml
import requests
from bs4 import BeautifulSoup


def get_link_product(url):
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.text, "lxml")
    title = soup.select_one("#productTitle").getText().strip()
    price = soup.select_one("#corePrice_feature_div").select_one(".a-offscreen").getText().strip('€')
    price = float(price.replace(',', '.'))

    return title, price