from urllib.parse import urljoin

from utils.request_util import get_html
from utils.html_util import (
    get_soup,
    get_text,
    get_attr
)


def search_news(keyword=None, page_num=1):
    """
    证券日报网-银行频道
    """

    if page_num == 1:
        url = "http://www.zqrb.cn/jrjg/bank/index.html"
    else:
        url = f"http://www.zqrb.cn/jrjg/bank/index_p{page_num}.html"

    soup = get_soup(get_html(url))

    result = []

    for li in soup.select("div.news_content ul li"):

        a = li.select_one("a.lista")

        if not a:
            continue

        title = get_text(a)

        if not title:
            continue

        publish_time = get_text(li.select_one("span.date"))

        result.append({
            "title": title,
            "publish_time": publish_time,
            "url": urljoin(url, get_attr(a, "href")),
            "source": "证券日报"
        })
        if len(result) >= 10:
            break

    return result


if __name__ == "__main__":

    news = search_news()

    for item in news:
        print(item)
