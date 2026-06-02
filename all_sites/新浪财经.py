from utils.request_util import get_html
from utils.html_util import (
    get_soup,
    get_text,
    get_attr
)


def search_news(keyword=None, page_num=1):
    """
    新浪财经-银行频道
    """

    url = "https://finance.sina.com.cn/roll/c/56684.shtml?page=1"

    soup = get_soup(get_html(url))

    result = []

    for li in soup.select("#listcontent li")[:30]:

        a = li.select_one("a")

        if not a:
            continue

        title = get_text(a)

        if not title:
            continue


        publish_time = get_text(li.select_one("span"))
        publish_time = (
            publish_time.replace("(", "")
            .replace(")", "")
            .replace("\xa0", "")
            .strip()
        )

        result.append({
            "title": title,
            "publish_time": publish_time,
            "url": get_attr(a, "href"),
            "source": "新浪财经"
        })

    return result


if __name__ == "__main__":

    news = search_news()

    for item in news:
        print(item)