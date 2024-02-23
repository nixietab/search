import requests
from bs4 import BeautifulSoup
from socket import gethostbyname

def get_ip_address(url):
    try:
        domain = url.split('//')[-1].split('/')[0]
        ip_address = gethostbyname(domain)
        return ip_address
    except Exception as e:
        print(f"Failed to get IP address for {url}. Error: {e}")
        return None

def get_page_description(soup):
    meta_description = soup.find('meta', attrs={'name': 'description'})
    if meta_description:
        return meta_description.get('content')
    else:
        return None

def save_to_file(url, ip_address, description, filename='webpages.txt'):
    try:
        with open(filename, 'a') as file:
            file.write(f"URL: {url}\nName: {ip_address['name']}\nIP: {ip_address['ip']}\nDescription: {description}\n\n")
        print(f"")
    except Exception as e:
        print(f"Failed to save data to {filename}. Error: {e}")

def simple_web_crawler(url, depth=1):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"Title: {soup.title.text}")
            print(f"URL: {url}")

            ip_address = {'name': soup.title.text, 'ip': get_ip_address(url)}
            description = get_page_description(soup)
            
            if ip_address['ip']:
                save_to_file(url, ip_address, description)

            if depth > 1:
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and href.startswith('http'):
                        simple_web_crawler(href, depth - 1)
        else:
            print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            save_to_file(url, {'name': 'Failed', 'ip': None}, None)
    except Exception as e:
        print(f"An error occurred while processing {url}. Error: {e}")
        save_to_file(url, {'name': 'Error', 'ip': None}, None)

url_to_crawl = 'URL TO START CRAWLING'
depth_to_crawl = 2
simple_web_crawler(url_to_crawl, depth_to_crawl)
