from urllib.parse import urljoin

from utils.request_util import get_html
from utils.html_util import (
    get_soup,
    get_text,
    get_attr
)


def search_news(keyword=None, page_num=1):
    """
    中国经济网-银行频道
    """

    if page_num == 1:
        url = "http://finance.ce.cn/bank/"
    else:
        url = f"http://finance.ce.cn/bank/index_{page_num - 1}.shtml"

    soup = get_soup(get_html(url))

    result = []

    for li in soup.select("ul.list2 li"):

        a = li.select_one("a")

        if not a:
            continue

        title = get_text(a)

        if not title:
            continue


        publish_time = get_text(li.select_one("span"))
        publish_time = publish_time.replace("[", "").replace("]", "").replace("\xa0", "").strip()

        result.append({
            "title": title,
            "publish_time": publish_time,
            "url": urljoin(url, get_attr(a, "href")),
            "source": "中国经济网"
        })

    return result


if __name__ == "__main__":

    news = search_news()

    for item in news:
        print(item)
