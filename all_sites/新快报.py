from urllib.parse import urljoin

from utils.request_util import get_html
from utils.html_util import (
    get_soup,
    get_text,
    get_attr
)


def search_news(keyword=None):
    """
    新快报-经济频道
    只取前20条
    """

    url = "https://www.xkb.com.cn/list/428"

    soup = get_soup(get_html(url))

    result = []

    # 所有文章链接
    articles = soup.select('a[href^="/articleDetail/"]')

    for a in articles:

        href = get_attr(a, "href")
        if not href:
            continue

        # 标题
        title_div = a.select_one("div.text-xl")
        title = get_text(title_div)

        if not title:
            continue


        # 日期
        publish_time = ""

        info_divs = a.select("div.text-gray-500 div")

        if len(info_divs) >= 2:
            publish_time = get_text(info_divs[1])

        result.append({
            "title": title,
            "publish_time": publish_time,
            "url": urljoin(url, href),
            "source": "新快报"
        })

        # 只保留前20条
        if len(result) >= 20:
            break

    return result


if __name__ == "__main__":

    news = search_news()

    for item in news:
        print(item)