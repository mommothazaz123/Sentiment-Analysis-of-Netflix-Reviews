import random

import requests
from bs4 import BeautifulSoup

NUM_TO_EXTRACT = 678
INDEX_URL = "https://www.dandwiki.com/wiki/5e_Magic_Items_by_Rarity"
API_BASE = "https://www.dandwiki.com"

index = requests.get(INDEX_URL)
index_soup = BeautifulSoup(index.text, 'html.parser')

all_items = []

rarity_tables = index_soup.find_all('table')[:4]
for table in rarity_tables:
    rows = table.findChildren('tr')

    for row in rows:
        links = row.findChildren('a')
        if not links:
            continue
        else:
            link = links[0].get('href')
            all_items.append(link)

random_items = random.sample(all_items, NUM_TO_EXTRACT)
out = []

for item in random_items:
    print(f"Getting {item}")
    response = requests.get(f"{API_BASE}{item}")
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        desc_table = soup.find_all('table')[0]
    except IndexError:
        random_items.append(random.choice(all_items))
        continue
    text = desc_table.get_text().strip().replace('\n', ' ')
    out.append(text)

with open('../raw/dnd-polarity.neg', 'w') as writer:
    writer.write('\n'.join(out))
