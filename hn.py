import requests
import time
from bs4 import BeautifulSoup

# Custom Hacker News. Analyzes first n pages and displays news 
# with score > points_min in a sorted order

custom_hn = []
n = 1    # Number of first pages
points_min = 200

print('/// Analysing pages:', end='')
for x in range(1,n+1):
    print(f' {x}', end='')
    res = requests.get('https://news.ycombinator.com/news?p='+ str(x))
    soup = BeautifulSoup(res.text, 'html.parser')

    ranks = soup.select('.rank')
    links = soup.select('.titleline')
    subtext = soup.select('.subtext')

    def get_custom_hn(ranks, links, subtext):
        for i,x in enumerate(links):
            rank = ranks[i].get_text().replace('.', '')
            title = x.get_text()
            href = x.find('a').get('href')    # None if not found
            score = subtext[i].select('.score')
            if score:
                points = int(score[0].get_text().replace(' points', ''))
                if points > points_min:
                    custom_hn.append({'rank': rank, 'title': title, 'link': href, 'points': points})
        return None

    get_custom_hn(ranks, links, subtext)

    time.sleep(1)

print()
print()
custom_hn = sorted(custom_hn, key = lambda k:k['points'], reverse = True)

# Display news with spaces
for x in custom_hn:
    print(x['rank'], '. ', x['title'], sep='')

    if len(x['rank']) == 1:
        print('  ', x['link'])
        print('   points:', x['points'])

    if len(x['rank']) == 2:
        print('   ', x['link'])
        print('    points:', x['points'])

    if len(x['rank']) == 3:
        print('    ', x['link'])
        print('     points:', x['points'])

    print()
