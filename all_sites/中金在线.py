from utils.request_util import get_html
from bs4 import BeautifulSoup


def search_news(keyword=None, page_num=1):

    url = "http://bank.cnfol.com/"

    html = get_html(url)

    soup = BeautifulSoup(html, "html.parser")

    news_list = []

    for block in soup.select("#artList .artBlock"):

        title_node = block.select_one("a.h3")

        if not title_node:
            continue

        title = title_node.get_text(strip=True)



        url = title_node.get("href", "")

        time_node = block.select_one(".artTime i")

        publish_time = ""

        if time_node:
            publish_time = time_node.get_text(strip=True)

        news_list.append({
            "title": title,
            "publish_time": publish_time,
            "url": url,
            "source": "中金在线",
        })

    return news_list


if __name__ == "__main__":

    news = search_news()

    for item in news:
        print(item)