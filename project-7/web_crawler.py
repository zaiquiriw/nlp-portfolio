from bs4 import BeautifulSoup
import requests
from collections import deque
from urllib import request

def webScrape(starter_url, keyword1, keyword2): 

    siteQueue = deque([starter_url])

    visited = set()

    with open('urls.txt', 'w') as f:
        counter = 0
        while counter < 30:
            currUrl = siteQueue.pop()
            visited.add(currUrl)
            r = requests.get(currUrl)
            data = r.text
            soup = BeautifulSoup(data, features="html.parser")
    # write urls to a file
            for currUrl in soup.find_all('a'):
                link_str = str(currUrl.get('href'))
                ##print(link_str)
                if keyword1 in link_str or keyword2 in link_str:
                    if link_str.startswith('/url?q='):
                        link_str = link_str[7:]
                        ##print('MOD:', link_str)
                    if '&' in link_str:
                        i = link_str.find('&')
                        link_str = link_str[:i]
                    if link_str.startswith('http') and 'google' not in link_str:
                        siteQueue.append(link_str)
                        f.write(link_str + '\n')
                        filename = f"{counter}textfile.txt"
                        with open(filename, 'w', encoding='utf-8') as f1:
                            try:
                                errResp = requests.get(link_str)
                                if errResp.status_code == 200:     
                                    with request.urlopen(link_str) as f2: 
                                        raw = f2.read().decode('utf-8-sig')
                                        soup2  = BeautifulSoup(raw, features="html.parser")
                                        p_tags = soup2.find_all('p')
                                        if(len(p_tags) > 0):
                                            for p in p_tags:
                                                f1.write(p.text)
                                                f1.write('\n')
                                            counter += 1
                                            if counter >= 30:
                                                break
                                else:
                                    print("http error")        
                            except requests.exceptions.HTTPError as error:
                                print("error: " + error)
                            except requests.exceptions.ConnectionError as error:
                                print("error: " + error)
    # end of program
    print("end of crawler")
            

starter_url = "https://en.wikipedia.org/wiki/Despicable_Me"
webScrape(starter_url, "Despicable", "despicable")
##textScraper("urls.txt")