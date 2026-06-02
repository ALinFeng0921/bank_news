import requests
from urllib.parse import quote


def search_news(keyword, page=0, pagesize=20):
    url = "https://www.yicai.com/api/ajax/getSearchResult"

    params = {
        "page": page,
        "pagesize": pagesize,
        "keys": keyword,
        "type": 1
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://www.yicai.com/search?keys={quote(keyword)}",
        "X-Requested-With": "XMLHttpRequest"
    }

    resp = requests.get(url, params=params, headers=headers)

    data = resp.json()

    result = []

    docs = data.get("results", {}).get("docs", [])

    for item in docs:

        news_url = item.get("url", "")

        # 补全相对路径
        if news_url.startswith("/"):
            news_url = "https://www.yicai.com" + news_url

        result.append({
            "title": item.get("title", ""),
            "publish_time": item.get("creationDate", ""),
            "source": item.get("source", ""),
            "url": news_url
        })

    return result
