from urllib.request import urlopen
from bs4 import BeautifulSoup

def extract_file(url, index):
    with urlopen(url) as response:
        html = response.read()
        html_str = html.decode('utf=8')
        # print(html_str)

        soup = BeautifulSoup(html_str.replace('\n', '').replace('\r', ''), 'html.parser')
        body = soup.body

        new_file_name = "webpages/url" + str(index) + '.txt'
        f = open(new_file_name, "w+")
        f.write(html_str)
        f.close()

# go through all the url's we are investigating in urls_list.txt
urls_file = open('urls_list.txt', 'r')
urls = urls_file.readlines()
for index, url in enumerate(urls):
    extract_file(url.strip(), index)