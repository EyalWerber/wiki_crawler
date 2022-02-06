from bs4 import BeautifulSoup as bs
import requests as r
# 'Fact' loops with 'true' and vise versa
# 'Latin' is a loop hole

base_url = 'https://en.wikipedia.org'

base_href = '/wiki/Special:Random'

LOOP_WIKIS = ['/wiki/Latin',
              '/wiki/Latin_language', '/wiki/Greek_language', '/wiki/Ancient_Greek_language', '/wiki/Ancient_Greece', 'Traditional_Chinese_characters', '/wiki/Descriptive_knowledge', '/wiki/Writing_system', '/wiki/Proposition', '/wiki/List_of_Latin_phrases', '/wiki/Classical_antiquity']
ALL_WIKIS = []


def get_first_wiki(anchor_list):
    for a in anchor_list:
        if(a['href'].find('/wiki/') > -1 and a['href'].find('IPA') == -1 and a['href'].find('File') == -1 and a['href'].find('https:') == -1):
            if(a['href'] in LOOP_WIKIS):
                continue
            return a['href'][a['href'].find('/wiki/'):]


def get_real_paragraph(paragraph_list):
    for p in paragraph_list:
        if not p.has_attr('class') and p.find('a'):
            return p


def soup_cleaner(soup):
    if(soup.find('div', {'class': "quotebox"})):
        soup.find('div', {'class': "quotebox"}).decompose()
    if(soup.findAll('table')):
        for table in soup.findAll('table'):
            table.decompose()
    if(soup.findAll('p', {'class': "mw-empty-elt"})):
        for p in soup.findAll('p', {'class': "mw-empty-elt"}):
            p.decompose()


def loop_check(href):
    if href in ALL_WIKIS:
        LOOP_WIKIS.append(href)
        print("LOOP!!!")
    else:
        ALL_WIKIS.append(href)


def recourse_hrefs(href):

    counter = 0
    while (href != '/wiki/Philosophy'):
        counter += 1
        res = r.get(base_url+href)

        soup = bs(res.content, features="lxml")
        soup_cleaner(soup)

        paragraph = get_real_paragraph(soup.find_all('p'))
        if(paragraph.find_all('a')):
            if(not get_first_wiki(paragraph.find_all('a'))):
                continue
            else:
                href = get_first_wiki(paragraph.find_all('a'))

        print(f'Iteration #{counter} - {href}')
        loop_check(href)

    print(f'FINISHED ON ITERATION {counter}')


recourse_hrefs(base_href)
