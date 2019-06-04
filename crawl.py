import requests
import bs4
import translate

example_url = 'https://www.refinery29.com/en-gb/george-rr-martin-requested-bran-become-king-game-of-thrones'


def crawl_one_page_process(url, raw=False):
    # page
    response = requests.get(url)
    page_soup = bs4.BeautifulSoup(response.text, "lxml")
    # article
    page_article = page_soup.body.main.article
    article_soup = bs4.BeautifulSoup(str(page_article), 'lxml')
    # title
    title_node = article_soup.findAll("div", {"class": "header"})
    title_soup = bs4.BeautifulSoup(str(title_node[0]), 'lxml')
    title = title_soup.findAll("h1", {"class": "title"})
    if raw:
        print(title[0].text)
    print(translate.googleTranslate(title[0].text))
    # content
    content_nodes = article_soup.findAll("div", {"id": "article-main-content"})
    content_soups = bs4.BeautifulSoup(str(content_nodes[0]), 'lxml')
    contents = content_soups.findAll("div", {"class": "section-text"})
    for content in contents:
        content_soup = bs4.BeautifulSoup(str(content), 'lxml')
        if raw:
            print(content_soup.text)
        print(translate.googleTranslate(content_soup.text))


if __name__ == '__main__':
    crawl_one_page_process(example_url, True)
