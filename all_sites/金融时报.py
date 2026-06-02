from urllib.parse import urljoin

from utils.request_util import get_html
from utils.html_util import (
    get_soup,
    get_text,
    get_attr
)


def search_news(keyword=None, page_num=1):

    if page_num == 1:
        url = "http://www.financialnews.com.cn/node_3005.html"
    else:
        url = f"http://www.financialnews.com.cn/node_3005_{page_num}.html"

    soup = get_soup(get_html(url))

    result = []

    for dl in soup.select("div.news-list dl"):

        a = dl.select_one("h4 a")

        title = get_text(a)

        if not title:
            continue


        result.append({
            "title": title,
            "publish_time": get_text(dl.select_one("h6 span")),
            "url": urljoin(url, get_attr(a, "href")),
            "source": "中国金融新闻网"
        })

    return result


if __name__ == "__main__":

    news = search_news()

    for i in news:
        print(i)