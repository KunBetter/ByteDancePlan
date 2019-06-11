import time
import requests
import bs4
import translate


def crawl_refinery29(url):
    # page
    response = requests.get(url)
    page_soup = bs4.BeautifulSoup(response.text, "lxml")
    # Latest News
    latest_news = []
    news_lists = page_soup.findAll("div", {"class": "slick-track"})
    news_lists_soup = bs4.BeautifulSoup(str(news_lists[0]), 'lxml')
    print('--------------Fetch Latest News----------')
    for content in news_lists_soup.div.contents:
        content_soup = bs4.BeautifulSoup(str(content), 'lxml')
        latest_news.append(url + str(content_soup.div.a['href']))
    print('Latest News Count : ' + str(len(latest_news)))
    # trending and now on R29
    print('--------------Fetch Trending and Now on R29----------')
    trending_and_now_on_r29 = []
    modules = page_soup.findAll("div", {"class": "module"})
    for module in modules:
        module_soup = bs4.BeautifulSoup(str(module), 'lxml')
        if module_soup.div.header is not None:
            '''
            # title
            head_soup = bs4.BeautifulSoup(str(module_soup.div.header), "lxml")
            title = head_soup.findAll("h2", {"class": "title"})
            print(title[0].text)
            '''
            # row
            row_div_soup = bs4.BeautifulSoup(str(module_soup.div), "lxml")
            rows = row_div_soup.findAll("div", {"class": "row"})
            if len(rows) > 0:
                for row in rows:
                    row_soup = bs4.BeautifulSoup(str(row), "lxml")
                    cards = row_soup.findAll("div", {"class": "card"})
                    for card in cards:
                        card_soup = bs4.BeautifulSoup(str(card), "lxml")
                        trending_and_now_on_r29.append(url + str(card_soup.div.a['href']))
                        '''
                        # section
                        card_section = card_soup.findAll("div", {"class": "section"})
                        card_section_soup = bs4.BeautifulSoup(str(card_section), "lxml")
                        print(str(card_section_soup.div.text))
                        # title
                        card_title = card_soup.findAll("div", {"class": "title"})
                        card_title_soup = bs4.BeautifulSoup(str(card_title), "lxml")
                        print(str(card_title_soup.span.text))
                        '''
    print('Trending and Now on R29 Count : ' + str(len(trending_and_now_on_r29)))
    fn = open("/Users/anthony/Desktop/R29.txt", "w")
    print('--------------Translating Latest News----------')
    progress_rate = 0
    latest_news_2 = list(set(latest_news))
    for resource in latest_news_2:
        print('Translating: ' + resource)
        url, title, cn_title, text, cn_text, cn_text_len = crawl_refinery29_detail_page(
            resource)
        progress_rate = progress_rate + 1
        if 0 < cn_text_len <= 1500:
            fn.write('=====================================================================================\n')
            fn.write('【原文链接】 ' + url + '\n')
            fn.write('【原文标题】 ' + title + '\n')
            fn.write('【谷歌翻译标题】 ' + cn_title + '\n')
            fn.write('【谷歌翻译正文字数】 ' + str(cn_text_len) + '\n')
            fn.write('【原文正文】\n' + text + '\n')
            fn.write('【谷歌翻译正文】\n' + cn_text + '\n')
        if progress_rate % 5 == 0:
            print('Has Translate ' + str(progress_rate) + ' pages ...')
        time.sleep(2)
    print('--------------Latest News Translate Done!----------')
    print('--------------Translating Trending and Now on R29----------')
    progress_rate = 0
    trending_and_now_on_r29_2 = list(set(trending_and_now_on_r29))
    for resource in trending_and_now_on_r29_2:
        print('Translating: ' + resource)
        url, title, cn_title, text, cn_text, cn_text_len = crawl_refinery29_detail_page(
            resource)
        progress_rate = progress_rate + 1
        if 0 < cn_text_len <= 1500:
            fn.write('=====================================================================================\n')
            fn.write('【原文链接】 ' + url + '\n')
            fn.write('【原文标题】 ' + title + '\n')
            fn.write('【谷歌翻译标题】 ' + cn_title + '\n')
            fn.write('【谷歌翻译正文字数】 ' + str(cn_text_len) + '\n')
            fn.write('【原文正文】\n' + text + '\n')
            fn.write('【谷歌翻译正文】\n' + cn_text + '\n')
        if progress_rate % 5 == 0:
            print('Has Translate ' + str(progress_rate) + ' pages ...')
        time.sleep(2)
    print('--------------Trending and Now on R29 Translate Done!----------')
    fn.close()


# {url,title,ch_title,text,cn_text,cn_text_len}
def crawl_refinery29_detail_page(url, debug=False):
    # page
    response = requests.get(url)
    page_soup = bs4.BeautifulSoup(response.text, "lxml")
    # article
    page_article = page_soup.body.main.article
    article_soup = bs4.BeautifulSoup(str(page_article), 'lxml')
    # title
    title_nodes = article_soup.findAll("div", {"class": "header"})
    if len(title_nodes) <= 0:
        return url, '', '', '', '', 0
    title_soup = bs4.BeautifulSoup(str(title_nodes[0]), 'lxml')
    title_node = title_soup.findAll("h1", {"class": "title"})
    title = title_node[0].text
    cn_title = translate.google_translate(title)
    # content
    content_nodes = article_soup.findAll("div", {"id": "article-main-content"})
    content_soup = bs4.BeautifulSoup(str(content_nodes[0]), 'lxml')
    contents = content_soup.findAll("div", {"class": "section-text"})
    text = ''
    text_len = 0
    text_2_translate = []
    for content in contents:
        content_soup = bs4.BeautifulSoup(str(content), 'lxml')
        text += content_soup.text + ' '
        text_len += len(content_soup.text)
        if text_len > 1500:
            text_2_translate.append(text)
            text = ''
            text_len = 0
    if text_len > 0:
        text_2_translate.append(text)
    text = ''
    cn_text = ''
    for t2t in text_2_translate:
        text += t2t
        cn_text += translate.google_translate(t2t)
    cn_text_len = len(cn_text)
    if debug:
        print(url, title, cn_title, text, cn_text, cn_text_len)
    return url, title, cn_title, text, cn_text, cn_text_len


if __name__ == '__main__':
    crawl_refinery29('https://www.refinery29.com')

    # refinery29_one_page_url = 'https://www.refinery29.com/en-us/2019/06/234807/unc-charlotte-shooting-survivor-mother-daughter-gun-violence'
    # crawl_refinery29_detail_page(refinery29_one_page_url, True)
