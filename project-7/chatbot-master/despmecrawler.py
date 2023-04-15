from bs4 import BeautifulSoup
import requests
import re
from collections import deque
from urllib import request


url = "https://despicableme.fandom.com/wiki/Category:Characters"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

member_links = soup.find_all("a", class_="category-page__member-link")

member_links_filtered = [link for link in member_links if "Category" not in link["href"]]

href_strings = []
for link in member_links_filtered:
    href_strings.append(str(link.get('href')))

prefix = "https://despicableme.fandom.com/"

absolute_links = [prefix + link for link in href_strings]

for link in absolute_links:
    print(link)



siteQueue = deque()

for link in absolute_links:
    siteQueue.append(link)

visited = set()

with open('characterwhoisfaq.txt', 'w', encoding="utf-8") as f:

    while len(siteQueue) > 0:
        url = siteQueue.pop()

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        paragraph = None

        for p in soup.find_all('p'):
            if p.find('b') is not None:
                all_text = p.text.strip()
                if all_text.count('\n') <= 1:
                    paragraph = p
                    break

        if paragraph is not None:
            bold_text = paragraph.find('b').text
            all_text = paragraph.text.strip()
            f.write("Who is " + bold_text + "?")
            f.write("\n")
            f.write(all_text)
            f.write("\n")
        else:
            print('No paragraph found with bold text')