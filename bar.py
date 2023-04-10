

def get_subheader_links(url_main_page):
    base_url = 'https://www.azrielimalls.co.il'
    links = []
    for url in url_main_page:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        subheader_items = soup.find_all('div', {'class': 'sub-header-item'})
        for item in subheader_items:
            href = item.find('a')['href'].strip()
            links.append(base_url + href)
    return links

def main_page_mall():
    
    url = 'https://www.azrielimalls.co.il/'
    base_url = 'https://www.azrielimalls.co.il/'
    r = requests.get(url)
    mall_soup = BeautifulSoup(r.text, 'html.parser')

    # Get all the mall names
    stores = []
    mall_section = mall_soup.find('div', {'class': 'my-malls-wrapper'})
    if mall_section is not None:
        mall_name = mall_section.find('img').get('alt')
        mall_url = url + mall_section.find('a').get('href')
        stores.append((mall_name, mall_url))
        for mall in mall_section.find_all('a'):
            mall_name = mall.get_text().strip()
            mall_url = base_url + mall.get('href')
            stores.append((mall_name, mall_url))

    # Get all the store URLs
    store_urls = []
    for mall in mall_section.find_all('a'):
        mall_name = mall.get_text().strip()
        mall_url = base_url + mall.get('href')
        store_urls.append(mall_url)
        
    return store_urls


x = get_subheader_links(url_main_page)
print(x)
