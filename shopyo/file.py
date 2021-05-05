import requests
from bs4 import BeautifulSoup
from pprint import pprint

site_url = 'https://defimedia.info/'
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
titles = requests.get(site_url, headers=header).content
moon_soup = BeautifulSoup(titles, 'html.parser')
rows = table.find_all('sup-title')
print(rows)