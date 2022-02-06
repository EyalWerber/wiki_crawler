from bs4 import BeautifulSoup as bs
import requests as r
# 'Fact' loops with 'true' and vise versa
# 'Latin' is a loop hole

base_url = 'https://en.wikipedia.org'

base_href = '/wiki/Special:Random'

LOOP_WIKIS = set()


def get_first_wiki(anchor_list):
    for a in anchor_list:
        if(a['href'].find('/wiki/') > -1 and a['href'].find('IPA') == -1 and a['href'].find('File') == -1 and a['href'].find('https:') == -1):
            if(a['href'] in LOOP_WIKIS):
                # print('SKIP!')
                continue
            return a['href'][a['href'].find('/wiki/'):]


def get_real_paragraphs(paragraph_list):
    for p in paragraph_list:
        if p.has_attr('class') and not p.find('a'):
            paragraph_list.remove(p)
    return paragraph_list


def soup_cleaner(soup):
    unwanted_elements = {'div': {'class': "quotebox"},
                         'p': {'class': "mw-empty-elt"}, 'table': {}}
    for key, value in unwanted_elements.items():
        if soup.find_all(key, value):
            for element in soup.find_all(key, value):
                element.decompose()


def loop_check(href):
    if href in LOOP_WIKIS:
        print("LOOP!!!")
    else:
        LOOP_WIKIS.add(href)


def crawl_hrefs(href):

    counter = 0
    while (href != '/wiki/Philosophy'):
        counter += 1
        res = r.get(base_url+href)

        soup = bs(res.content, features="lxml")
        soup_cleaner(soup)
        paragraph_li_list = get_real_paragraphs(soup.find_all(
            'p')) + get_real_paragraphs(soup.find_all('li'))

        for paragraph in paragraph_li_list:
            if paragraph.find('a'):
                if(not get_first_wiki(paragraph.find_all('a'))):
                    # if no anchor tags were found, go to next paragraph
                    continue
                else:
                    href = get_first_wiki(paragraph.find_all('a'))
                    break

        print(f'Iteration #{counter} - {href}')
        loop_check(href)

    print(f'FINISHED ON ITERATION {counter}')


# crawl_hrefs('/wiki/Verification')
crawl_hrefs(base_href)
