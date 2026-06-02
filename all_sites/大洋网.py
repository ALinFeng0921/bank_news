from bs4 import BeautifulSoup
from utils.request_util import get_html


def search_news(keyword="", page_num=1):
    """
    广州日报大洋网
    """

    url = "https://life.dayoo.com/money/154563.shtml"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/136.0 Safari/537.36"
        )
    }

    html = get_html(url, headers=headers)

    soup = BeautifulSoup(html, "html.parser")

    result = []

    news_list = soup.find_all("div", class_="news-item")

    for item in news_list:
        try:
            a_tag = item.find("h2").find("a")

            title = a_tag.get_text(strip=True)
            news_url = a_tag["href"]

            abst_tag = item.find("div", class_="news-abst")
            time_tag = item.find("div", class_="news-time")

            summary = abst_tag.get_text(strip=True) if abst_tag else ""
            publish_time = time_tag.get_text(strip=True) if time_tag else ""

            # 关键词过滤
            # if keyword:
            #     all_text = f"{title} {summary}"
            #
            #     if keyword not in all_text:
            #         continue

            result.append({
                "title": title,
                "publish_time": publish_time,
                "url": news_url,
                "source": "广州日报大洋网"
            })

        except Exception as e:
            print("解析失败：", e)

    return result
