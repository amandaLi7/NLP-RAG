from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# RUN FILE USING python3 process_html.py

# from https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python 
def extract_plaintext(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def extract_file(url, index):
    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urlopen(req) as response:
        html = response.read()
        html_str = html.decode('utf=8')
        # print(html_str)

        soup = BeautifulSoup(html_str, 'html.parser')
        html_str = extract_plaintext(soup)

        new_file_name = "webpages/url" + str(index) + '.txt'
        f = open(new_file_name, "w+")
        f.write(html_str)
        f.close()

        print("---- " + url + " DONE -------")

# go through all the url's we are investigating in urls_list.txt
urls_file = open('urls_list.txt', 'r')
urls = urls_file.readlines()
for index, url in enumerate(urls):
    extract_file(url.strip(), index)